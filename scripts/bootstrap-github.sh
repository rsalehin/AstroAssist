#!/usr/bin/env bash
# Creates the public GitHub repo rsalehin/AstroAssist and pushes the initial commit.
# Requires: git, and either `gh` (authenticated) or a GITHUB_TOKEN env var.
set -euo pipefail
OWNER=rsalehin; REPO=AstroAssist
cd "$(dirname "$0")/.."
git init -b main 2>/dev/null || true
git add -A
git commit -m "chore: initial specification, architecture, ADRs and implementation plan" 2>/dev/null || echo "nothing to commit"
if command -v gh >/dev/null 2>&1; then
  gh repo view "$OWNER/$REPO" >/dev/null 2>&1 || gh repo create "$OWNER/$REPO" --public --description "Provenance-first, multi-agent research workbench for astronomers" --disable-wiki
  git remote get-url origin >/dev/null 2>&1 || git remote add origin "https://github.com/$OWNER/$REPO.git"
elif [ -n "${GITHUB_TOKEN:-}" ]; then
  curl -fsS -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user/repos \
    -d "{\"name\":\"$REPO\",\"private\":false,\"description\":\"Provenance-first, multi-agent research workbench for astronomers\"}" >/dev/null || true
  git remote get-url origin >/dev/null 2>&1 || git remote add origin "https://$GITHUB_TOKEN@github.com/$OWNER/$REPO.git"
else
  echo "Install gh (https://cli.github.com) and run 'gh auth login', or export GITHUB_TOKEN." >&2; exit 1
fi
git push -u origin main
echo "Pushed to https://github.com/$OWNER/$REPO"
