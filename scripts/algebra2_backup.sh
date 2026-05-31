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

# VM 전용 local git identity. Global 설정은 건드리지 않는다.
git config user.name "GFIELD VM Bot"
git config user.email "docssam1+gfield-vm-bot@gmail.com"

mkdir -p backups
BACKUP_FILE="backups/index_base_${STAMP}.html"
cp index.html "$BACKUP_FILE"
git add "$BACKUP_FILE"

if git diff --cached --quiet; then
  echo "ALGEBRA2 BACKUP SKIPPED"
  echo "Reason: no staged changes"
  exit 0
fi

git commit -m "Backup algebra2 index ${STAMP}"
git push origin main

echo "ALGEBRA2 BACKUP DONE"
echo "Created: $BACKUP_FILE"
echo "Commit: $(git log -1 --oneline)"
