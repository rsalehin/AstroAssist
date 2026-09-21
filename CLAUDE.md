# CLAUDE.md — instructions for Claude Code

You are implementing **AstroAssist**, an open-source, locally-run, multi-agent research workbench for astronomers. Read this file fully before touching code.

## 0. First-run bootstrap (do this once)

If the GitHub repo does not exist yet:

```bash
bash scripts/bootstrap-github.sh   # creates public repo rsalehin/AstroAssist, first commit, push
```

Then set up the dev environment:

```bash
uv sync --all-extras          # or: pip install -e ".[dev]"
uv run pytest                 # smoke tests must pass
```

## 1. Read these before implementing anything

In order: `docs/PRODUCT.md` → `docs/ARCHITECTURE.md` → `docs/DATA_MODEL.md` → `docs/AGENTS.md` → `docs/SOURCES.md` → `docs/IMPLEMENTATION_PLAN.md`. The feature IDs in `docs/FEATURES.md` (e.g. `F-CORE-003`) are the vocabulary for commits, PRs and issues. ADRs in `docs/adr/` are binding unless superseded by a new ADR.

## 2. Non-negotiable engineering rules

1. **No naked numbers.** Every physical quantity is an `astropy.units.Quantity` (or `SkyCoord`, `Time`, `QTable`). Dimensionless is the only exception. Unit conversion is done by Astropy, never by the LLM.
2. **No artifact without provenance.** Every scientific output is a typed artifact (`src/astroassist/core/artifacts.py`) with a `Provenance` record. A tool that returns a bare float or string is a bug.
3. **Agents return artifacts, not prose.** Only the final synthesis node produces natural language, and it cites artifact IDs.
4. **Sources are tools; agents are reasoning roles.** Do not create one agent per archive. See `docs/AGENTS.md`.
5. **Every external query is inspectable.** Store the generated ADQL/URL/params/raw response in a `QueryArtifact`. The UI shows it collapsed by default.
6. **Curated tools before generated code.** Add a typed tool to `src/astroassist/tools/` before reaching for the Python escape hatch. Generated Python always goes through the HITL approval interrupt.
7. **Be polite to public archives.** Every connector declares a `RatePolicy`. Never call live services in unit tests — use recorded fixtures in `tests/fixtures/`. Live contract tests are marked `@pytest.mark.live` and excluded by default.
8. **Reproducibility is a feature.** Every action must be expressible as `typed action + inputs + code/tool + output + provenance` so the session can be exported as a runnable bundle (`docs/REPRODUCIBILITY.md`).
9. **Secrets never touch disk in plaintext.** Credentials go through `CredentialManager` (OS keyring → env var → session). Never log tokens; never send them to LangSmith.
10. **Windows must not break.** Core package installs on Windows/macOS/Linux. Platform-limited packages live in optional extras only.

## 3. Tech stack (fixed by ADRs)

- Python `>=3.11,<3.14`, packaged with `uv` + `pyproject.toml`; `environment.yml` mirrors it for conda users.
- Backend: FastAPI + uvicorn, SSE/WebSocket streaming. Persistent per-workspace analysis kernel (jupyter_client).
- Orchestration: LangGraph (state graph, SQLite checkpointer, interrupts for HITL). LangChain tool abstractions. LangSmith tracing (opt-in; redacted).
- Models: pluggable `ModelProvider` protocol — Anthropic, OpenAI, OpenAI-compatible, Ollama, vLLM. Profiles: economy / balanced / research / local.
- Science: astropy, astroquery, pyvo, numpy, scipy, matplotlib, lightkurve, astroplan. Optional extras: photutils, specutils, regions, reproject, healpy, plotly, emcee, dynesty, gala, spectral-cube, sunpy.
- Storage: DuckDB (artifact catalog + analytics over Parquet), SQLite (LangGraph checkpoints + workspace metadata), filesystem (FITS/ECSV/Parquet/SVG/PNG).
- Frontend: React + TypeScript + Vite, Tailwind, TanStack Query, Zustand; Aladin Lite embedded; Plotly optional; matplotlib SVG default. Lives in `frontend/`. Built assets are served by the FastAPI app.
- Quality: ruff (lint + format), mypy (strict on `core/`), pytest, pytest-recording/vcr for fixtures, pre-commit.

## 4. Repository layout

```
src/astroassist/
  core/        artifacts, provenance, units, coords, errors, config, credentials
  sources/     one package per connector (simbad/, gaia/, vizier/, mast/, ads/ …) implementing SourcePlugin
  tools/       typed deterministic tools (resolve, cone_search, convert_units, distance, lomb_scargle, plot_*)
  agents/      object_catalog, observation, literature, time_domain, spectroscopy, compute, visualization, supervisor, planner, router, synthesis
  workflows/   LangGraph graph definitions, state schema, checkpointing, interrupts
  workspace/   workspace/session/thread/artifact store (DuckDB + SQLite + files), cache, jobs
  server/      FastAPI app, routes, streaming, static frontend
  eval/        benchmark runner, deterministic evaluators, LangSmith integration
  cli.py       `astroassist serve|workspace|eval|export`
frontend/      React workbench
tests/         unit (fixtures), contract (live, opt-in), benchmark
evals/         benchmark question sets (YAML)
docs/          product + architecture docs, ADRs
```

## 5. How to work

- Work in vertical slices following `docs/IMPLEMENTATION_PLAN.md`. Finish a slice end-to-end (tool → artifact → API → UI card → test) before starting the next.
- Before adding a connector run `/new-connector <id>`; before adding a tool run `/add-tool <name>` (see `.claude/commands/`).
- Conventional commits with feature IDs: `feat(sources): add SIMBAD resolver [F-SRC-001]`.
- Keep `docs/` in sync: if you change an interface described in a doc, update the doc in the same PR. If a design decision changes, write a new ADR — don't edit an accepted one.
- Do not integrate more than the MVP sources (SIMBAD, Gaia, VizieR, MAST, ADS) before M2 is complete and the benchmark passes.
- When unsure about a scientific convention (frames, epochs, magnitude systems, parallax zero-point), stop and add a note to `docs/OPEN_QUESTIONS.md` rather than guessing.

## 6. Definition of done for any feature

- Typed artifact(s) defined and serializable (Pydantic + Arrow/Parquet where tabular).
- Provenance populated and validated.
- Unit test with recorded fixture; contract test if live service involved.
- Exposed via API route and rendered by a UI card (or explicitly marked backend-only in the PR).
- Included in the reproducibility export (code + data + citation).
- Feature ID marked as done in `docs/FEATURES.md`.

## 7. Autonomous mode (continuous implementation with minimal human action)

The repo is set up so a session can run item after item without approval prompts:
- `.claude/settings.json` allow-lists uv/npm/git/pytest etc. and denies destructive commands and secret files.
- Hooks: `SessionStart` injects `docs/PROGRESS.md`; `PostToolUse` formats/lints every edited file; `Stop` runs `make check` and refuses to let the session end while it is red or while a `current:` item is open (capped at 6 forced continuations).
- `scripts/autopilot.sh` (or `make autopilot MILESTONE=M1`) loops headless sessions, one plan item each, pushing after every green commit, until `milestone_complete: <M>` appears in PROGRESS.md.
- Prompts: `.claude/prompts/first-run.md` (first session), `.claude/prompts/next-item.md` (loop).

Rules in this mode:
1. `docs/PROGRESS.md` is the only state that survives sessions. Keep it accurate: `Done`, `Current`, `Needs Abir`, `Notes for next session`. Set `blocked: true` only when nothing in the milestone can proceed.
2. Tests first, at every layer the item touches (see `docs/TESTING.md`). `make check` must be green before commit.
3. Decide from the docs; never wait for a human on scope, naming or structure. Genuine decisions go under `Needs Abir` with the safe default you took.
4. Never skip, delete or weaken a test to go green.
5. One item per session in the loop; commit and push after each. Small, reviewable commits with feature IDs.
6. Never touch `.env`, credentials, or force-push.

PROGRESS.md template:
```
# Progress
milestone: M0
blocked: false
## Done
## Current
- [ ] current: (none)
## Needs Abir
## Notes for next session
```
