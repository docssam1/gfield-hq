#!/usr/bin/env bash
set -euo pipefail

BASE="$HOME/gfield-projects"
REPO="$BASE/algebra2"
REMOTE="https://github.com/docssam1/algebra2.git"

mkdir -p "$BASE"

if [ ! -d "$REPO/.git" ]; then
  echo "Cloning algebra2..."
  git clone "$REMOTE" "$REPO"
fi

cd "$REPO"
git fetch origin main --quiet || true

echo "ALGEBRA2 STATUS"
echo "Repo: $(pwd)"
echo "Branch: $(git branch --show-current 2>/dev/null || echo unknown)"
echo "Local: $(git log -1 --oneline 2>/dev/null || echo none)"
echo "Remote main: $(git log origin/main -1 --oneline 2>/dev/null || echo none)"
echo "Working tree:"
git status --short || true
echo "Key files:"
ls -lh index.html 2>/dev/null || true
if [ -d backups ]; then
  ls -lh backups 2>/dev/null | tail -10 || true
else
  echo "backups: none"
fi
