# Testing strategy (continuous, no-human-in-the-loop)

Every implementation-plan item ships with tests at each layer it touches. `make check` is the single gate; the Stop hook refuses to end a session while it is red.

| Layer | Tool | Scope | Runs |
|---|---|---|---|
| Lint / types | ruff, mypy, eslint, tsc | everything | every edit (hook) + `make check` |
| Unit | pytest + pytest-recording fixtures | tools, connectors (normalization, provenance), artifacts, coords, units, cache, kernel | every `make check`, CI |
| Component | vitest + React Testing Library | every card and panel renders from a fixture artifact; actions fire | `make check`, CI |
| E2E | Playwright against `astroassist serve --profile mock` | day-one story steps as they land: message → stream → cards → approval → export | `make check`, CI |
| Contract | pytest `-m live` | one small live query per source | nightly, manual |
| Benchmark | `astroassist eval run evals/benchmark/` | scientific correctness with deterministic evaluators | before release, manual |

## Determinism: the `mock` model provider
`ModelProvider` adapter `mock` replays scripted responses from `tests/e2e/scripts/<scenario>.yaml` (router intent, planner DAG, synthesis text with artifact ids) keyed by a hash of the incoming prompt role + step. Combined with recorded archive fixtures, the whole request path runs offline with no keys. Every e2e scenario has a matching script; adding a UI step means adding a script step.

## Rules
- No live network in unit/component/e2e. Fixtures are recorded once with `uv run pytest --record-mode=once -m live` and committed.
- Component tests use artifact fixtures in `frontend/src/test/fixtures/` generated from the Python models (`astroassist eval fixtures --ts`) so UI and backend share the same shapes.
- Playwright uses `webServer` config to launch the backend with `ASTROASSIST_MODEL_PROFILE=mock` and a temp workspace dir.
- A failing test is never skipped or deleted to go green; fix the cause or record the blocker in `docs/PROGRESS.md`.
