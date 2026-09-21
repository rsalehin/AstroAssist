# Agents and orchestration

## Principle
**Sources are tools. Agents are reasoning roles.** Agents are split by scientific information/task domain, never one per archive.

## Roles
| Agent | Responsibility | Tools / sources (v1 → later) |
|---|---|---|
| Router | classify intent, pick profile | cheap model |
| Planner | build explicit DAG of typed steps, declare inputs/outputs, estimate cost | strong model + tool registry + schema registry |
| Object & Catalog | identity, astrometry, photometry, catalog cone/ADQL, crossmatch | SIMBAD, Sesame, Gaia, VizieR → NED, IRSA, SDSS, Pan-STARRS |
| Observation | find/download reduced observation products, inspect FITS | MAST → ESO, HEASARC, ALMA/NRAO, CADC |
| Literature | papers, citations, bibliography, local library evidence | ADS → arXiv, local RAG |
| Time-Domain | light curves, periodograms, flares, phase folding | lightkurve/MAST → ZTF, AAVSO, TNS |
| Spectroscopy (M4) | line lists, continuum, EW, line ID | NIST, VALD, specutils, CHIANTI, AtomDB |
| Compute | curated deterministic tools; propose Python for the escape hatch | Astropy, SciPy, astroplan |
| Visualization | plot spec construction and edits; typed plot tools; Aladin state | matplotlib, Plotly, Aladin Lite |
| Supervisor | detect failures, bounded self-correction, replanning, fallback with explicit reporting | |
| Synthesis | final answer from artifact summaries; cites artifact ids; flags disagreements | strong model |

## LangGraph design
State (`workflows/state.py`):
```python
class ResearchState(TypedDict):
    thread_id: str
    messages: list[AnyMessage]
    resolved_objects: dict[str, str]        # name → artifact id
    plan: PlanArtifact | None
    step_results: dict[str, list[str]]      # step id → artifact ids
    pending_interrupt: InterruptPayload | None
    trace: list[TraceEntry]
    errors: list[StepError]
    profile: ModelProfile
```
Graph: `ingest → resolve → route → plan → preflight ─(interrupt?)→ execute[parallel branches] → supervise ─(replan?)→ synthesize → persist`.

- Checkpointer: SQLite (`langgraph-checkpoint-sqlite`), thread id = chat thread.
- Interrupts (`interrupt()`): `large_query`, `large_download`, `proprietary_data`, `run_code`, `overwrite_delete`, `external_export`, `scientific_assumption`.
- Parallel branches via `Send` for independent steps (e.g. Gaia + 2MASS + WISE).
- Retries: query errors → schema-aware correction ×2 → surface. Never loop on external services.
- Streaming: `astream_events` → SSE mapping to UI event schema.

## Tool contract
```python
@tool(args_schema=ConeSearchInput)
def gaia_cone_search(...) -> CatalogTable: ...
```
- Input schema: Pydantic with units declared (`radius: Angle`).
- Output: one artifact (or list); raw payload written to disk; `QueryArtifact` created for external calls.
- Registered in `tools/registry.py` with domain tag, cost estimator, risk class.
- Cost estimator returns `{queries, est_rows, est_bytes, est_seconds}` for preflight.

## Prompting rules
- System prompts live in `agents/prompts/*.md` and are versioned.
- Agents receive artifact **summaries**, tool schemas, and the schema registry excerpt relevant to the step — never raw tables.
- Synthesis must reference numbers only via artifact ids (`{{art_…}}`); a post-check rejects numerals not traceable to an artifact.

## Model profiles
| Profile | Router | Planner | Synthesis |
|---|---|---|---|
| economy | small | mid | mid |
| balanced | small | strong | strong |
| research | mid | strong | strong |
| local | ollama small | ollama large | ollama large |

## Failure and fallback policy
- Source down → try capability-equivalent fallback; report "X unavailable; Y used; Z NOT retrieved".
- Disagreement beyond combined uncertainty → `disagreement` flag on artifacts; banner in UI.
- Unknown scientific convention → interrupt `scientific_assumption` rather than guess.
