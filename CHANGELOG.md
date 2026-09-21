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
