#!/usr/bin/env bash
# Fast feedback after every file edit: format + lint the touched file only. Never blocks; feeds warnings back.
cd "$(dirname "$0")/../.."
INPUT=$(cat)
FILE=$(printf '%s' "$INPUT" | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d.get("tool_input",{}).get("file_path",""))' 2>/dev/null)
[ -z "$FILE" ] && exit 0
case "$FILE" in
  *.py)
    uv run ruff format "$FILE" >/dev/null 2>&1
    OUT=$(uv run ruff check --fix "$FILE" 2>&1) || { echo "ruff issues in $FILE:"; echo "$OUT"; exit 2; }
    ;;
  *.ts|*.tsx)
    if [ -f frontend/package.json ]; then (cd frontend && npx --no-install prettier --write "../$FILE" >/dev/null 2>&1 || true); fi
    ;;
esac
exit 0
