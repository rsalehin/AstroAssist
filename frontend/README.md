# AstroAssist frontend

React + TypeScript + Vite + Tailwind workbench. Three-pane layout (rail / chat / artifact
viewer), SSE chat streaming, a generic artifact card, and a settings panel. Dark theme default;
light theme via the header toggle. See docs/UI_UX.md and docs/ARCHITECTURE.md (SSE event schema).

## Develop

```bash
npm install            # or: npm ci
npm run dev            # Vite dev server on http://127.0.0.1:5173 (proxies /api → :8765)
```

Run the backend in another terminal so the proxy has a target:

```bash
uv run astroassist serve --profile mock   # http://127.0.0.1:8765
```

## Test

```bash
npm run lint           # eslint (flat config)
npm run build          # tsc --noEmit + vite build
npm run test           # vitest + React Testing Library (component)
npm run test:e2e       # Playwright; launches the mock backend + dev server automatically
```

All of these run from the repo root via `make check`.

## Fixtures

Component fixtures in `src/test/fixtures/artifacts.ts` are generated from the Python artifact
models so the UI and backend share the same shapes:

```bash
uv run astroassist eval fixtures --ts --out frontend/src/test/fixtures/artifacts.ts
```

Design tokens live in `src/theme/tokens.ts` and `src/index.css` (CSS variables per theme).
