# Changelog
## Unreleased
- Project specification, architecture, ADRs and implementation plan (2026-09-21).
- Cross-platform dev setup: `make setup` installs core+dev; `make setup-all` for full stack; ruff excludes Markdown; `.gitattributes` keeps hooks LF.
- Package scaffold finalized: `astroassist version` CLI + tests [F-CORE-001/002].
- Core types: astropy JSON codecs (`QuantityValue`/`SkyCoordValue`/`TimeValue`), `Provenance` + id helpers, and all DATA_MODEL artifact kinds with a discriminated union [F-CORE-003/004].
- Config (`config.toml` + `ASTROASSIST_*` env), `CredentialManager` (keyring > env > session), and redacted structured logging [F-CORE-007/008/009].
- Workspace store: SQLModel metadata (workspace/session/thread/message/artifact-index/job), on-disk artifact layout, and a DuckDB artifact catalog [F-WS-001/002].
- Model providers: `ModelProvider` protocol, role/profile config, Anthropic/OpenAI/OpenAI-compatible/Ollama/vLLM adapters, error hierarchy [F-CORE-005].
- Deterministic `mock` provider (scripted from code or YAML) and `astroassist eval fixtures --ts` [F-EVAL-001].
- Tool registry (domain, risk class, cost estimator) and the `echo` tool returning a `ScientificValue` [F-AG-016].
- LangGraph skeleton (ingest→route→execute→synthesize) with SQLite checkpointer and HITL interrupt payloads [F-AG-001/013].
- FastAPI server with SSE streaming (trace/artifact/token/done), workspace/thread/artifact/interrupt/settings routes, and a working `astroassist serve --profile mock` [F-CORE-001].
- React/TS/Vite/Tailwind workbench: three-pane layout, SSE chat, generic artifact card, settings panel, dark/light themes [F-UI-001/002/016/018].
- Frontend test harness: vitest + React Testing Library component tests and a Playwright e2e (mock backend) asserting the echo artifact card, wired into `make check` [F-EVAL-005].
- CI matrix (Linux/macOS/Windows × Python 3.11/3.12/3.13) plus frontend + e2e jobs, with run concurrency; LangSmith tracing opt-in wiring [F-EVAL-005][F-COMM-001/002][F-AG-015].
- **Milestone M0 complete**: `hello` → echo tool → streamed artifact card in the UI, checkpoint persisted, deterministic mock provider, full test pyramid green.
