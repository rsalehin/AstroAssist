# Progress (state file for autonomous sessions — keep it short and current)

milestone: M0
milestone_complete: M0
blocked: false

## Done
- [x] M0-1 Package scaffold — CLI (`version`/`serve`), ruff/mypy/pytest config, pre-commit, CLI tests (2026-09-22)
- [x] M0-2 Core types — `core/units.py` (Quantity/SkyCoord/Time JSON codecs), `core/provenance.py`, `core/artifacts.py` (all DATA_MODEL kinds + discriminated union), round-trip tests, mypy strict green (2026-09-22)
- [x] M0-3 Config + credentials — `core/config.py` (pydantic-settings, TOML, env precedence), `core/credentials.py` (keyring>env>session), `core/logging.py` (structlog + secret redaction) (2026-09-22)
- [x] M0-4 Workspace store — `workspace/store.py` (SQLModel: workspace/session/thread/message/artifact-index/job + artifact file layout), `workspace/catalog.py` (DuckDB) (2026-09-22)
- [x] M0-5 Model providers — `core/models/` protocol + profiles + Anthropic/OpenAI/OpenAI-compatible/Ollama/vLLM adapters; `core/errors.py` (2026-09-22)
- [x] M0-5b Mock provider + fixtures CLI — `core/models/mock.py` (scripted, YAML), `astroassist eval fixtures --ts`, `eval/fixtures.py` (2026-09-22)
- [x] M0-6 Tool registry + echo — `tools/registry.py` (domain/risk/cost), `tools/echo.py` → `ScientificValue` (2026-09-22)
- [x] M0-7 LangGraph skeleton — `workflows/state.py`, `workflows/graph.py` (ingest→route→execute→synthesize + SQLite checkpointer), `workflows/interrupts.py` (run_code/large_query payloads) (2026-09-22)
- [x] M0-8 Server — `server/app.py` (`create_app`), routes (chat SSE, workspaces, threads, artifacts, interrupts, settings, bootstrap, health), `server/stream.py` (ARCHITECTURE event schema), `astroassist serve --profile mock` boots and streams the echo round-trip (2026-09-22)

- [x] M0-9 Frontend shell — Vite+React+TS+Tailwind three-pane workbench, SSE chat, generic `ArtifactCard`, settings panel, dark/light tokens (2026-09-22)
- [x] M0-9b Test harness — vitest+RTL component tests, Playwright e2e (mock backend + Vite dev) asserting the echo artifact card; wired into `make check` (2026-09-22)
- [x] M0-10 CI + hygiene — CI matrix (Linux/macOS/Windows × 3.11/3.12/3.13 + frontend + e2e) green; `concurrency` added; community files + templates + labels present; LangSmith opt-in wiring [F-COMM-001/002][F-EVAL-005][F-AG-015] (2026-09-22)

## Current
- [ ] current: (none)

## Needs Abir
<!-- decisions or credentials required; work continues with the stated safe default -->
- ANTHROPIC_API_KEY (or another provider key) for non-mock runs — default: all tests use the `mock` provider.
- ADS token for live ADS contract tests — default: skipped.
- `make setup` now installs **core + dev only** (`uv sync --extra dev`); the optional `dynamics` extra (gala/galpy) does **not** compile from source on Windows. Full scientific stack: `make setup-all` / `uv sync --all-extras` on a platform with a C/C++ toolchain. Safe default taken so the Windows dev loop and CI stay green. Not needed for M0–M1.

## Notes for next session
- Repo root is the **nested** `D:\Projects\AstroAssist\AstroAssist` (git root + `.claude/`). Work from there.
- ruff excludes `*.md`/`docs` (it reformats fenced code blocks in Markdown, which would rewrite spec docs).
