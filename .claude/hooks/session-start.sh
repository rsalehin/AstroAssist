#!/usr/bin/env bash
# Injects current progress and the next task into context at session start.
cd "$(dirname "$0")/../.."
echo "=== AstroAssist autonomous session ==="
echo "Read CLAUDE.md §7 (autonomous mode). Current progress:"
[ -f docs/PROGRESS.md ] && sed -n '1,80p' docs/PROGRESS.md
echo "Next unfinished item in docs/IMPLEMENTATION_PLAN.md is the one after the last 'done' entry in PROGRESS.md."
exit 0
