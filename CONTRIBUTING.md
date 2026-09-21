# Contributing

Thanks for helping build a research tool astronomers can trust.

## Setup
```bash
git clone https://github.com/rsalehin/AstroAssist && cd AstroAssist
uv sync --all-extras          # or: pip install -e ".[dev]"
pre-commit install
uv run pytest                 # unit tests (fixtures only)
uv run pytest -m live         # optional: live contract tests
cd frontend && npm install && npm run dev
```

## Ground rules
- Read `CLAUDE.md` §2 — the same engineering rules apply to humans.
- Every physical number is an Astropy `Quantity`; every artifact has provenance.
- Never call live services in unit tests; record fixtures.
- Reference a feature ID (`docs/FEATURES.md`) in your PR title: `feat(sources): VizieR cone search [F-SRC-004]`.
- Keep docs in sync in the same PR. Design changes need an ADR.

## Most valuable contributions
1. Source connectors — follow `docs/PLUGIN_SPEC.md` and use the `/new-connector` scaffold.
2. Curated tools with tests.
3. Benchmark questions with known answers (`evals/benchmark/`).
4. Fixtures for edge-case archive responses.

## Pull requests
Small, focused, tested. Fill the PR template. CI must pass on Linux, macOS and Windows.

## Code of conduct
See CODE_OF_CONDUCT.md.
