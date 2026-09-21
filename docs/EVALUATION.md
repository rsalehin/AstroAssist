# Evaluation strategy

Deterministic evaluators dominate LLM judges for scientific quantities.

## Layer 1 — deterministic unit tests (every PR)
Recorded fixtures (`tests/fixtures/<source>/*.yaml` via pytest-recording) for Gaia VOTable/JSON, SIMBAD, VizieR, MAST, ADS responses. Test parsing, unit mapping, provenance population, error handling, all curated tools, coordinate parsing, serialization round-trips. No live network.

## Layer 2 — source contract tests (nightly / manual)
`@pytest.mark.live`: SIMBAD resolves Vega; Gaia TAP_SCHEMA loads and a TOP 5 query works; MAST returns expected columns for AD Leo; ADS auth works with a token; VizieR cone search returns known catalog. Run via `uv run pytest -m live`.

## Layer 3 — astronomy benchmark (M3, grows to 100–300 questions)
`evals/benchmark/*.yaml`. Each item stores: question, expected source selection, expected tool calls (shape), expected query structure, expected answer with unit and tolerance, provenance requirements. Examples: resolve M31; Vega parallax; TESS data for AD Leo; distance from parallax; M87 redshift; crossmatch coordinates against Gaia; plot a TESS light curve; observability from Tautenburg.

Deterministic checks:
```python
assert result.unit == u.pc
assert abs(result.value - expected) < tol
assert result.provenance.source == "Gaia DR3"
assert result.provenance.query_id is not None
```

## Layer 4 — agent-quality metrics (LangSmith)
source-selection accuracy · tool-call correctness · query validity rate · artifact completeness · provenance completeness · citation correctness · numeric and unit correctness · trajectory efficiency · unnecessary-tool-call rate · failure-recovery rate · approval-gate compliance · cost per question. LLM judges only for prose quality of synthesis. Regression runs on curated datasets before each release.

## CI matrix
ruff + mypy + pytest on Python 3.11/3.12/3.13 × ubuntu/macos/windows. Frontend: tsc + eslint + vitest. Live and benchmark suites on schedule/manual dispatch only.
