# AstroAssist — reference & presentation site

Self-contained, dependency-free webpages describing AstroAssist. Every file is standalone
(inline CSS/JS, no build step, no CDN) — **copy this folder anywhere** (a static host, an
intranet share, a USB stick) and open the HTML directly.

| File | What it is |
|---|---|
| `index.html` | Landing page linking to the two documents |
| `reference.html` | Full technical reference — architecture, request lifecycle, data-flow, data model & provenance, agents, tech-stack, repo layout, roadmap, testing, and an illustrative deployment / CI-CD / DevOps plan |
| `presentation.html` | 14-slide deck (arrow keys / space to navigate, `F` fullscreen, `T` theme; deep-links via `#<n>`) |

Both pages have a light/dark theme toggle (remembered per browser) and are responsive.

## View locally

Just open `index.html` in a browser. To serve the folder over HTTP instead:

```bash
python -m http.server 8080 --directory docs/site
# then open http://localhost:8080/
```

## Regenerate / edit

The pages are hand-authored HTML derived from the docs in `../` (`PRODUCT.md`,
`ARCHITECTURE.md`, `DATA_MODEL.md`, `AGENTS.md`, `ROADMAP.md`, `FEATURES.md`). The
**Deployment**, **CI/CD** and **DevOps** sections are illustrative recommendations (deployment
is not yet implemented) for a local, ~20-user install.
