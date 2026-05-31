#!/usr/bin/env bash
set -euo pipefail

BASE="$HOME/gfield-projects"
REPO="$BASE/algebra2"
REMOTE="git@github-algebra2:docssam1/algebra2.git"
STAMP="$(date +%Y%m%d_%H%M%S)"
DIFF_DIR="$BASE/_diff_backups"

mkdir -p "$BASE" "$DIFF_DIR"
if [ ! -d "$REPO/.git" ]; then
  git clone "$REMOTE" "$REPO"
fi

cd "$REPO"

if ! git diff --quiet || [ -n "$(git status --short)" ]; then
  git diff > "$DIFF_DIR/algebra2_dirty_${STAMP}.diff" || true
  git status --short > "$DIFF_DIR/algebra2_dirty_${STAMP}.status" || true
  echo "Dirty state saved: $DIFF_DIR/algebra2_dirty_${STAMP}.diff"
fi

git fetch origin main --quiet
git reset --hard origin/main
git clean -fd

echo "ALGEBRA2 CLEAN DONE"
echo "Commit: $(git log -1 --oneline)"
echo "Status:"
git status --short || true
