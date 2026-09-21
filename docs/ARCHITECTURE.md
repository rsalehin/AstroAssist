# Architecture

## Context and goals
Single-user, locally-run research workbench. Hard requirements: correctness, provenance, reproducibility, inspectability, politeness to public archives, pluggable LLMs, extensibility via a plugin spec. See PRODUCT.md and the ADRs.

## High-level design

```
                    ┌──────────────────────────────┐
                    │  Browser workbench (React)    │
                    │  rail · chat · artifact viewer│
                    └──────────────┬───────────────┘
                     HTTP + SSE/WS │ JSON artifacts
                    ┌──────────────▼───────────────┐
                    │  FastAPI server                │
                    │  routes · streaming · static   │
                    └──────────────┬───────────────┘
                                   │
     ┌─────────────────────────────▼──────────────────────────────┐
     │  Orchestration (LangGraph)                                  │
     │  router → planner (DAG) → executor → supervisor → synthesis │
     │  SQLite checkpointer · interrupts (HITL) · LangSmith traces  │
     └───┬──────────┬──────────┬──────────┬──────────┬─────────────┘
         │          │          │          │          │
   Object&Catalog Observation Literature TimeDomain Compute/Vis   ← agents (reasoning roles)
         │          │          │          │          │
   SIMBAD Gaia    MAST ESO    ADS Local  lightkurve Astropy/SciPy ← tools & source plugins
   VizieR NED     HEASARC     RAG        ZTF AAVSO  matplotlib/Plotly
         └──────────┴──────────┴──────────┴──────────┘
                                   │
                    ┌──────────────▼───────────────┐
                    │  Typed artifacts + provenance  │
                    └──────────────┬───────────────┘
                                   │
          ┌────────────────────────┼────────────────────────┐
          ▼                        ▼                        ▼
   Workspace store           Analysis kernel           Research trace
   DuckDB + SQLite + files   (jupyter_client)          (per-step log)
```

## Request lifecycle
1. **Ingest** — message arrives with thread id; artifacts referenced via `@id` are attached.
2. **Resolve** — any new identifier hits the Object Resolver (session cache → SIMBAD → Sesame → NED if extragalactic context).
3. **Route** — cheap model classifies intent (identity / catalog / observation / literature / compute / plot / plan / mixed / chit-chat).
4. **Plan** — planner emits an explicit DAG of typed steps with declared inputs/outputs; parallel branches allowed. The plan itself is stored as an artifact.
5. **Preflight** — each step's connector estimates cost (queries, rows, bytes, duration). Steps exceeding thresholds create a LangGraph interrupt for approval.
6. **Execute** — steps run as LangGraph nodes; tools return typed artifacts; raw payloads stored on disk and referenced by id (never dumped into model context).
7. **Supervise** — failures trigger bounded self-correction (max 2 for query errors) or replanning; capability-aware fallback with explicit "not retrieved" reporting.
8. **Synthesize** — strong model writes the answer using artifact summaries only, citing artifact ids; UI expands ids into cards.
9. **Persist & trace** — artifacts, queries, code and trace entries stored in workspace; bibliography updated.

## Tech stack
| Layer | Choice | ADR |
|---|---|---|
| Language/packaging | Python 3.11–3.13, uv, pyproject, environment.yml | ADR-0001 |
| Runtime | Local FastAPI + browser UI; Tauri later | ADR-0002 |
| Orchestration | LangGraph + LangChain tools + LangSmith | ADR-0003 |
| Models | pluggable ModelProvider; profiles | ADR-0004 |
| Scientific types | astropy Quantity/SkyCoord/Time/QTable | ADR-0005 |
| Storage | DuckDB + SQLite + files | ADR-0006 |
| Computation | curated tools + approved Python in persistent kernel | ADR-0007 |
| Agent split | by scientific domain/task; sources are tools | ADR-0008 |
| Visualization | matplotlib default via plot spec; Plotly optional | ADR-0009 |
| UI | workbench (React/TS/Vite) | ADR-0010 |
| Credentials | OS keyring | ADR-0011 |
| Aladin Lite | embedded, GPL-3 kept separate | ADR-0012 |
| Evaluation | fixtures + contract + benchmark + LangSmith | ADR-0013 |

## Backend modules
- `core/` — `artifacts.py` (Pydantic models), `provenance.py`, `units.py` (serialization of Quantity/SkyCoord/Time), `coords.py` (input parsing), `config.py`, `credentials.py`, `errors.py`, `rate.py`.
- `sources/` — `base.py` (`SourcePlugin`, `Manifest`, `RatePolicy`, `SchemaProvider`), one subpackage per connector, `registry.py`.
- `tools/` — LangChain `@tool`s with Pydantic input schemas returning artifacts; grouped by domain.
- `agents/` — node factories per role; prompts in `agents/prompts/`.
- `workflows/` — `state.py` (typed graph state), `graph.py` (build graph), `interrupts.py`, `planner_schema.py`.
- `workspace/` — `store.py`, `catalog.py` (DuckDB), `cache.py`, `jobs.py`, `kernel.py`, `bibliography.py`, `export.py`.
- `server/` — `app.py`, `routes/{chat,workspace,artifacts,jobs,settings,credentials}.py`, `stream.py`.
- `eval/` — `runner.py`, `evaluators.py`, `langsmith.py`.

## API surface (v1)
- `POST /api/threads/{id}/messages` (SSE stream of events: token, artifact, interrupt, trace, done)
- `POST /api/interrupts/{id}/resolve` (approve / edit / cancel)
- `GET /api/workspaces`, `POST /api/workspaces`, `GET /api/workspaces/{id}/artifacts`
- `GET /api/artifacts/{id}`, `GET /api/artifacts/{id}/data` (Arrow/Parquet/CSV), `GET /api/artifacts/{id}/code`
- `POST /api/queries/{id}/rerun`
- `GET /api/jobs`, `POST /api/jobs/{id}/cancel`
- `GET/PUT /api/settings`, `PUT /api/credentials/{source}`
- `POST /api/workspaces/{id}/export` → bundle zip
- `POST /api/kernel/{ws}/restart`, `GET /api/kernel/{ws}/variables`

## Streaming event schema
```json
{"type":"artifact","artifact":{"id":"art_…","kind":"ScientificValue","summary":{…}}}
{"type":"interrupt","interrupt_id":"…","reason":"large_query","payload":{…}}
{"type":"trace","step":"query_gaia","source":"Gaia","duration_ms":1400,"query_id":"q_…"}
{"type":"token","text":"…"}
{"type":"done","message_id":"…"}
```

## Security and safety
- Generated Python only runs after approval, in the workspace kernel, with resource limits and a workspace-scoped filesystem.
- Credentials via keyring; redacted from logs and LangSmith; never in artifacts.
- Rate policies and circuit breakers per source; global concurrency cap.
- No arbitrary URLs: connectors only call their declared endpoints.

## Key trade-offs
- Curated tools limit flexibility but make determinism, provenance and evaluation possible; the escape hatch restores flexibility with a human gate.
- A plot *spec* layer is extra work but makes plot edits reproducible and avoids regenerating arbitrary code.
- Planner + DAG is heavier than a plain ReAct loop, but gives parallelism, preflight cost estimates and an inspectable plan artifact.
