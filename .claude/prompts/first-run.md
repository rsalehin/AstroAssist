This is the first session on AstroAssist. Read CLAUDE.md in full, then docs/PRODUCT.md, docs/ARCHITECTURE.md, docs/DATA_MODEL.md, docs/AGENTS.md, docs/TESTING.md and docs/IMPLEMENTATION_PLAN.md. Do not summarize them back to me.

Then, without asking me questions:
1. Run `bash scripts/bootstrap-github.sh` to create the public repo rsalehin/AstroAssist and push. If it fails because gh is not authenticated, stop and tell me exactly what to run.
2. Run `make setup`, then `make check-fast`, and fix anything that fails.
3. Create docs/PROGRESS.md from the template in CLAUDE.md §7 if it is missing.
4. Work through milestone M0 in docs/IMPLEMENTATION_PLAN.md one item at a time: tests first, implement, `make check` green, tick FEATURES.md, CHANGELOG, commit with feature IDs, push. Keep going item after item; do not stop to ask for approval on scope you can decide from the docs. Put anything that truly needs me under "Needs Abir" in PROGRESS.md and continue with a safe default.
5. Include from the start: the `mock` ModelProvider (scripted from YAML) so every test and e2e run is deterministic and needs no API key; the frontend scaffold with vitest + React Testing Library + Playwright wired into `make check`; the Playwright e2e that starts `astroassist serve --profile mock` and checks the echo round-trip renders an artifact card.
When M0's exit check passes, write `milestone_complete: M0` in PROGRESS.md and give me a short report: what was built, what is under "Needs Abir", and the command to start M1 (`make autopilot MILESTONE=M1`).
