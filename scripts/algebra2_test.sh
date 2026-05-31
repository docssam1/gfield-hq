#!/usr/bin/env bash
set -euo pipefail

BASE="$HOME/gfield-projects"
REPO="$BASE/algebra2"
APP_URL="https://docssam1.github.io/algebra2/"
HEALTH_URL="https://algebra2-gemini-proxy-v2-274099580288.asia-northeast3.run.app/api/health"

cd "$REPO"

echo "ALGEBRA2 TEST"
echo "Commit: $(git log -1 --oneline)"
echo "Working tree:"
git status --short || true

echo "App URL check:"
curl -I -L --max-time 15 "$APP_URL" | head -10 || true

echo "Cloud Run health:"
curl -sS --max-time 15 "$HEALTH_URL" | head -20 || true

echo "HTML sanity:"
grep -n "downloadMaterialPack" index.html | head -5 || true
grep -n "renderDynamicTextReport" index.html | head -5 || true
grep -n "setOmrValue" index.html | head -5 || true
