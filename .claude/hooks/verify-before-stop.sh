#!/usr/bin/env bash
# Runs the full verification gate before Claude is allowed to stop.
# Exit 2 = "not done, keep working" (stderr is fed back to Claude). Exit 0 = allowed to stop.
cd "$(dirname "$0")/../.."
INPUT=$(cat)
ACTIVE=$(printf '%s' "$INPUT" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("stop_hook_active", False))' 2>/dev/null)
# Loop guard: at most N forced continuations per session.
COUNTER=.claude/.stop-continuations
N=$(cat "$COUNTER" 2>/dev/null || echo 0)
MAX=${ASTROASSIST_MAX_CONTINUATIONS:-6}
if [ "$ACTIVE" = "True" ] && [ "$N" -ge "$MAX" ]; then
  echo "Continuation cap ($MAX) reached; stopping. Record blockers in docs/PROGRESS.md." >&2; rm -f "$COUNTER"; exit 0
fi
# Nothing changed since last commit and tree clean → fine to stop.
if git diff --quiet && git diff --cached --quiet && [ -z "$(git status --porcelain)" ]; then rm -f "$COUNTER"; exit 0; fi
LOG=$(mktemp)
if make check >"$LOG" 2>&1; then
  if grep -q "^- \[ \] current:" docs/PROGRESS.md 2>/dev/null; then
    echo $((N+1)) > "$COUNTER"
    echo "All checks pass but docs/PROGRESS.md still has an open 'current:' item. Finish it: mark done, update docs/FEATURES.md + CHANGELOG.md, commit with feature IDs, then git push." >&2
    exit 2
  fi
  rm -f "$COUNTER" "$LOG"; exit 0
else
  echo $((N+1)) > "$COUNTER"
  echo "Verification failed (make check). Fix before stopping. Last 60 lines:" >&2
  tail -60 "$LOG" >&2; rm -f "$LOG"; exit 2
fi
