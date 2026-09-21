# Implementation plan (M0 → M1, ordered)

Claude Code: execute in order, one PR per numbered item, each with tests. Mark feature IDs done in FEATURES.md.

## M0
1. **Package scaffold** — `pyproject.toml` (already present), `src/astroassist/__init__.py`, `cli.py` with `serve`, `version`; ruff/mypy/pytest config; pre-commit. [F-CORE-001/002, F-EVAL-005]
2. **Core types** — `core/units.py` (Quantity/SkyCoord/Time JSON codecs), `core/provenance.py`, `core/artifacts.py` (all kinds in DATA_MODEL.md), round-trip tests. [F-CORE-003/004]
3. **Config + credentials** — `core/config.py` (pydantic-settings, `~/.astroassist/config.toml`), `core/credentials.py` (keyring → env → session), redaction in logging. [F-CORE-007/008/009]
4. **Workspace store** — `workspace/store.py` (SQLite via SQLModel/SQLAlchemy: workspace, session, thread, message, artifact index, job), `workspace/catalog.py` (DuckDB over Parquet), artifact file layout. [F-WS-001/002]
5. **Model providers** — `core/models.py` `ModelProvider` protocol; adapters using langchain-anthropic, langchain-openai (also OpenAI-compatible), langchain-ollama; profile config. [F-CORE-005]
5b. **Mock model provider + fixtures CLI** — `core/models/mock.py` replays scripted responses from `tests/e2e/scripts/*.yaml`; `astroassist eval fixtures --ts` exports artifact fixtures for the frontend. [F-EVAL-001]
6. **Tool registry** — `tools/registry.py`: register `@tool`s with domain, risk class, cost estimator; `tools/echo.py` stub returning `ScientificValue`. [F-AG-016]
7. **LangGraph skeleton** — `workflows/state.py`, `workflows/graph.py` (ingest → route(stub) → execute(echo) → synthesize), SQLite checkpointer, `interrupts.py` with `run_code` and `large_query` payloads. [F-AG-001/013]
8. **Server** — `server/app.py`, routes for threads/messages (SSE), artifacts, interrupts, workspaces, settings; event schema from ARCHITECTURE.md. [F-CORE-001]
9. **Frontend shell** — Vite + React + TS + Tailwind; three-pane layout, chat with SSE streaming, generic artifact card, settings page, dark/light tokens. [F-UI-001/002/016/018]
9b. **Test harness** — vitest + React Testing Library component tests for the generic card; Playwright config with `webServer` launching `astroassist serve --profile mock`; first e2e: send message → echo artifact card visible. Wire into `make check`. [F-EVAL-005]
10. **CI + hygiene** — GitHub Actions matrix; issue/PR templates already present; CHANGELOG. [F-COMM-001/002]

Exit check: send "hello" → echo tool → artifact card streams to UI; checkpoint persisted; run visible in LangSmith when enabled.

## M1
11. **SourcePlugin base** — `sources/base.py`, `sources/registry.py`, manifest loader, `core/rate.py` (limiter, backoff, circuit breaker). [F-SRC-000/020]
12. **SIMBAD connector** — resolve, aliases, basic data, bibliography; `ResolvedObject`; fixtures; contract test; Sesame fallback. [F-SRC-001/002, F-Q-001]
13. **Coordinate parsing** — `core/coords.py` all input forms → SkyCoord; tests. [F-Q-002]
14. **Object resolver node** — session cache, runs before routing. [F-WS-003]
15. **Schema registry** — `sources/schema_registry.py`: TAP_SCHEMA mirror in DuckDB with timestamps; `astroassist schemas refresh`. [F-SRC-019]
16. **Gaia connector** — single object, cone, ADQL sync/async; quality flags; `QueryArtifact` with raw response; ADQL self-correction ×2; cost estimator. [F-SRC-003, F-Q-007/008/009]
17. **Compute tools** — convert_units, coordinate_transform, distance_from_parallax, tangential_velocity, space_velocity; provenance lineage. [F-TOOL-001..004]
18. **Source-selection policy + planner** — router (cheap model), planner emitting `PlanArtifact` DAG with `Send` parallelism; preflight thresholds → interrupts. [F-AG-002/003, F-Q-003/005]
19. **Object & Catalog + Compute + Visualization agents** — node factories, prompts. [F-AG-005/006/007]
20. **Plot spec + matplotlib** — `tools/plots/spec.py`, theme, scatter/line/light-curve tools, `PlotArtifact` with code+data. [F-VIS-001/002/008]
21. **Kernel + escape hatch** — `workspace/kernel.py` (jupyter_client), `run_code` interrupt flow, `CodeArtifact`. [F-WS-007, F-TOOL-015]
22. **Synthesis node** — artifact-id citation, numeral post-check. [F-AG-012]
23. **Cache** — per-source TTL, key spec, modes. [F-WS-004/005]
24. **UI cards** — object, scientific value, table (paged), query (edit & rerun), plot (show code), code approval dialog. [F-UI-003..007, 012, 013]
25. **Benchmark seed** — 20 questions in `evals/benchmark/m1.yaml` with deterministic checks. [F-EVAL-001/002]

Exit check: "What is the distance and tangential velocity of AD Leo, in light-years and km/s?" → resolver → Gaia → tools → value cards with lineage → ADQL card editable → plot of the cone-search field.
