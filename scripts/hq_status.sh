#!/usr/bin/env bash
set -euo pipefail

cd /home/gfield7265/gfield-hq

echo "=== GFIELD HQ STATUS ==="
echo "[git]"
git status --short
git log -3 --oneline

echo
echo "[service]"
systemctl status gfield-bot.service --no-pager -l | sed -n '1,12p'

echo
echo "[registered commands]"
grep -n "ALLOWED_CMDS" -A40 bot_runner.py
