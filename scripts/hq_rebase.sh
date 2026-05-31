#!/usr/bin/env bash
set -euo pipefail

cd /home/gfield7265/gfield-hq

echo "=== GFIELD HQ REBASE ==="
git status --short
git fetch origin main
git rebase origin/main
git status --short
git log -3 --oneline
