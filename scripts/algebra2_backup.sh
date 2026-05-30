#!/usr/bin/env bash
set -euo pipefail

BASE="$HOME/gfield-projects"
REPO="$BASE/algebra2"
REMOTE="https://github.com/docssam1/algebra2.git"
STAMP="$(date +%Y%m%d_%H%M%S)"

mkdir -p "$BASE"

if [ ! -d "$REPO/.git" ]; then
  echo "Cloning algebra2..."
  git clone "$REMOTE" "$REPO"
fi

cd "$REPO"
git pull --ff-only origin main
mkdir -p backups
cp index.html "backups/index_base_${STAMP}.html"
git add "backups/index_base_${STAMP}.html"
git commit -m "Backup algebra2 index ${STAMP}"
git push origin main

echo "ALGEBRA2 BACKUP DONE"
echo "Created: backups/index_base_${STAMP}.html"
echo "Commit: $(git log -1 --oneline)"
