# Progress (state file for autonomous sessions — keep it short and current)

milestone: M0
blocked: false

## Done
<!-- - [x] M0-1 Package scaffold (2026-09-22) -->

## Current
- [ ] current: (none)

## Needs Abir
<!-- decisions or credentials required; work continues with the stated safe default -->
- ANTHROPIC_API_KEY (or another provider key) for non-mock runs — default: all tests use the `mock` provider.
- ADS token for live ADS contract tests — default: skipped.
- `make setup` now installs **core + dev only** (`uv sync --extra dev`); the optional `dynamics` extra (gala/galpy) does **not** compile from source on Windows. Full scientific stack: `make setup-all` / `uv sync --all-extras` on a platform with a C/C++ toolchain. Safe default taken so the Windows dev loop and CI stay green. Not needed for M0–M1.

## Notes for next session
- Repo root is the **nested** `D:\Projects\AstroAssist\AstroAssist` (git root + `.claude/`). Work from there.
- ruff excludes `*.md`/`docs` (it reformats fenced code blocks in Markdown, which would rewrite spec docs).
