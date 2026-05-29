#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."
echo "GFIELD HQ STATUS"
echo "Repo: $(pwd)"
echo "Branch: $(git branch --show-current 2>/dev/null || echo unknown)"
echo "Last commit: $(git log -1 --oneline 2>/dev/null || echo none)"
echo "Files:"
find . -maxdepth 2 -type f | sort | sed 's#^./#- #' | head -80
