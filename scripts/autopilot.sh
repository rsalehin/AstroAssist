#!/usr/bin/env bash
# Runs Claude Code headlessly, one implementation-plan item per iteration, until the milestone is done.
# Usage: bash scripts/autopilot.sh [MILESTONE=M0] [MAX_ITER=40]
# Requires: claude (Claude Code CLI) authenticated, uv, node. Recommended: run inside a container/VM.
set -uo pipefail
MILESTONE=${1:-${MILESTONE:-M0}}
MAX_ITER=${2:-${MAX_ITER:-40}}
cd "$(dirname "$0")/.."
for i in $(seq 1 "$MAX_ITER"); do
  if grep -q "^milestone_complete: $MILESTONE" docs/PROGRESS.md 2>/dev/null; then echo "$MILESTONE complete."; exit 0; fi
  echo "=== autopilot iteration $i ($MILESTONE) ==="
  PROMPT=$(sed "s/{{MILESTONE}}/$MILESTONE/g" .claude/prompts/next-item.md)
  claude -p "$PROMPT" --dangerously-skip-permissions --max-turns 250 --output-format text 2>&1 | tee -a .claude/autopilot.log
  git push origin HEAD 2>/dev/null || true
  if grep -q "^blocked: true" docs/PROGRESS.md 2>/dev/null; then echo "Blocked — see 'Needs Abir' in docs/PROGRESS.md"; exit 3; fi
done
echo "Max iterations reached."; exit 4
