.PHONY: setup lint typecheck unit component e2e live check check-fast serve autopilot
setup:      ; uv sync --all-extras && pre-commit install && ( [ -f frontend/package.json ] && cd frontend && npm ci && npx playwright install --with-deps chromium || true )
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
