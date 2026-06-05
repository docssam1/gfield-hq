#!/usr/bin/env bash
set -euo pipefail

BASE="$HOME/gfield-projects"
REPO="$BASE/algebra2"
REMOTE="git@github-algebra2:docssam1/algebra2.git"

mkdir -p "$BASE"
if [ ! -d "$REPO/.git" ]; then
  git clone "$REMOTE" "$REPO"
fi

cd "$REPO"
echo "ALGEBRA2 DIFF"
echo "Repo: $(pwd)"
echo "Commit: $(git log -1 --oneline)"
echo "Status:"
git status --short || true
echo "Diff stat:"
git diff --stat || true
echo "Recent commits:"
git log --oneline -5 || true
