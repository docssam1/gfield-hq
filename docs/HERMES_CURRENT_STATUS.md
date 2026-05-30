# HERMES_CURRENT_STATUS

Last updated: 2026-05-30 KST

## 1. Purpose

This document is the handoff/status record for the G-FIELD Hermes Command Center.
It exists so another GPT, Gemini, developer, or future server environment can continue the work even if the current chat slows down or stops.

## 2. Core Principle

G-FIELD Hermes is not a single chatbot.
It is the operating command system for G-FIELD.

- Telegram = fast mobile remote controller
- Hermes Web Dashboard = full admin control panel, planned
- GCP VM/VPS = 24-hour execution server
- GitHub = code and deployment record
- Google Drive = files, reports, PDFs, videos, materials
- Google Sheets = student, consultation, tuition, attendance, task DB
- GPT/Gemini = AI brains for different tasks

The owner should be able to ask in Korean from mobile or PC, and Hermes should route the work.

## 3. Known Accounts and Repositories

### GitHub

- GitHub account: docssam1
- Repository: https://github.com/docssam1/gfield-hq
- Main branch: main

### Google Cloud

- Active project ID used for VM: project-56629b95-34aa-49fc-8cf
- Project name shown in console: My First Project
- Related account/project context: gfield7265
- Other listed project: gen-lang-client-0995737435 / Default Gemini Project

### Google Drive

- Main Drive data owner: docssam1 account
- gfield7265 account and/or service account access should be shared to the main Drive folders.
- Service account access is required for automated VM/API Drive scans.

### Telegram

- Telegram bot has been created.
- Telegram numeric owner ID recorded during setup: 7844283061
- Bot token must NOT be stored in GitHub or this document.
- Token is stored in VM .env file.

## 4. Current Server State

### GCP VM

- VM name: gfield-hq-vm
- Zone: asia-northeast3-a
- Machine type at creation/check: e2-small
- External IP observed: 34.64.222.189
- Internal IP observed: 10.178.0.2
- Status observed: RUNNING

### Bot Service

- Service name: gfield-bot.service
- systemd path: /etc/systemd/system/gfield-bot.service
- Working directory: /home/gfield7265/gfield-hq
- Python venv: /home/gfield7265/gfield-hq/venv
- Environment file: /home/gfield7265/gfield-hq/.env
- Service state observed: active (running)
- Enabled on boot: yes

### Verified Telegram Command

- /run status works.
- It returns repository path, branch, last commit, and file listing.

## 5. Current Repository Contents

Important files currently known:

- bot_runner.py
- requirements.txt
- README.md
- frontend/index.html
- api/main.py
- scripts/status.sh
- scripts/status.ps1
- scripts/deploy.ps1
- .github/workflows/deploy.yml

Notes:

- GitHub Actions workflow currently exists but Cloud Run deployment is not fully configured yet.
- Earlier workflow failure was due to premature build/deploy assumptions and missing package/GCP secrets.
- Do not treat GitHub Actions failure as core system failure. Telegram/VM foundation works.

## 6. Completed Work

- GitHub repository created and pushed.
- Initial file scaffold added.
- Telegram bot created.
- Owner ID restriction added conceptually through OWNER_ID.
- VM created on Google Cloud.
- Repository cloned on VM.
- Python venv installed on VM.
- Bot dependencies installed.
- .env file created on VM.
- systemd service created and enabled.
- Telegram /run status confirmed.

## 7. Important Problems Encountered and Resolved

### Problem: Cloud Shell vs VM confusion

Cloud Shell is temporary and does not use systemd.
The 24-hour bot must run on VM, not Cloud Shell.

### Problem: PowerShell command on Linux

Initial bot_runner.py tried to run PowerShell.
Cloud Shell/VM are Linux, so runner must use bash.

### Problem: Multiple bot instances

Telegram Conflict/getUpdates error happened when both Cloud Shell and VM ran the same bot.
Correct rule: only VM systemd should run the bot.

### Problem: Token exposure risk

Bot tokens were visible during troubleshooting.
Rule: never store token in GitHub or documentation. If exposed, revoke/regenerate from BotFather.

## 8. Current Priority

Immediate priority is not more infrastructure for its own sake.
The priority is:

1. Drive API authentication and full Drive inventory
2. Report automation data gathering
3. Homepage premium rebuild
4. Project Memory System
5. Telegram command expansion
6. Hermes Web Dashboard later

## 9. Planned Telegram Commands

Current:

- /run status
- /run deploy, limited/pull-style command

Planned:

- /run drive_scan
- /run report_inventory
- /run kakao_analyze
- /run homepage_build
- /run report_build
- /run memory_status

## 10. Data and Privacy Rules

- Student data must not be stored in GitHub.
- GitHub is only for code and system documentation.
- Drive stores files, reports, videos, PDFs.
- Sheets stores operation DB: students, attendance, tuition, consultation, task status.
- Telegram is a command channel, not the permanent file database.
- Child photos/videos should be stored in Drive/Storage with controlled access, not public GitHub.

## 11. Credit and Cost Strategy

Known credit situation from console screenshots/conversation:

- Google Cloud Free Trial credit: about KRW 442,623 observed.
- GenAI App Builder / GenAI credit: about KRW 1,475,511 observed.
- Total visible credit context around KRW 1.9M.

Interpretation:

- Free Trial credit likely supports VM, Cloud Run, Storage, normal GCP services.
- GenAI credit likely supports Gemini/Vertex/GenAI App Builder style workloads.
- Exact service applicability and expiration must be verified in Billing/Credits console.

Strategy:

- First 3 months: build quickly using GCP/Cloud Run/API where useful.
- 1-year/longer server or VPS: keep Telegram bot, n8n, always-on jobs.
- After initial build: move stable always-on work to cheaper VPS if needed.
- Keep Cloud Run for scalable API/webhook jobs if cost is acceptable.

## 12. Final Target Architecture

Owner speaks in Korean through Telegram or Hermes Web.
Hermes Command Center receives the request, searches memory, routes work to GPT/Gemini/GitHub/Drive/Sheets/Cloud/VM, saves outputs, and reports back.

Final identity:

G-FIELD Hermes = G-FIELD operation OS.
