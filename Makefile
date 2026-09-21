.PHONY: setup setup-all lint typecheck unit component e2e live check check-fast serve autopilot
# Default dev setup: core + dev only. Cross-platform (some science extras, e.g. `dynamics`/gala,
# compile from source and do not build on Windows). Install the full scientific stack with
# `uv sync --all-extras` on a platform with a C/C++ toolchain when you need those packs.
setup:      ; uv sync --extra dev && uv run pre-commit install && ( [ -f frontend/package.json ] && cd frontend && npm ci && npx playwright install --with-deps chromium || true )
setup-all:  ; uv sync --all-extras && uv run pre-commit install && ( [ -f frontend/package.json ] && cd frontend && npm ci && npx playwright install --with-deps chromium || true )
lint:       ; uv run ruff check . && uv run ruff format --check . && ( [ -f frontend/package.json ] && cd frontend && npm run lint || true )
typecheck:  ; uv run mypy && ( [ -f frontend/package.json ] && cd frontend && npx tsc --noEmit || true )
unit:       ; uv run pytest -q
component:  ; ( [ -f frontend/package.json ] && cd frontend && npx vitest run || echo "frontend not scaffolded" )
e2e:        ; ( [ -f frontend/package.json ] && cd frontend && npx playwright test || echo "e2e not scaffolded" )
live:       ; uv run pytest -m live
check-fast: lint typecheck unit
check:      lint typecheck unit component e2e
serve:      ; uv run astroassist serve
autopilot:  ; bash scripts/autopilot.sh
