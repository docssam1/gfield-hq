#!/usr/bin/env bash
set -euo pipefail

cd /home/gfield7265/gfield-hq

echo "=== GFIELD HQ SAFE DEPLOY ==="
echo "[1] fetch origin main"
git fetch origin main

echo "[2] rebase origin/main"
git rebase origin/main

echo "[3] restart telegram bot"
sudo systemctl restart gfield-bot.service

echo "[4] status"
git status --short
git log -3 --oneline
echo "bot: $(systemctl is-active gfield-bot.service)"
