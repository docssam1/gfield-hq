# GFIELD Hermes Worker Handoff

Last updated: 2026-06-02 KST

## 1. Operating Rule

GFIELD Hermes is controlled from one command center.

- Command center VM: `gfield-hq-vm`
- Worker / API VM: `gfield-core-vm`
- Telegram bot process: run only on `gfield-hq-vm`
- GitHub repository: `docssam1/gfield-hq`

Do not run the same Telegram bot token from multiple VMs. If the bot is running on `gfield-core-vm`, stop and disable it.

```bash
sudo systemctl stop gfield-bot.service
sudo systemctl disable gfield-bot.service
```

## 1.1 New Worker Onboarding Rule

This document is the official new-worker onboarding program for GFIELD Hermes.

Every new worker must do the following before touching code, VM, Drive, or Telegram commands:

1. Read this file first.
2. Identify their assigned section.
3. Report which section they are working on.
4. Run only the commands assigned to that section.
5. If a new command, server role, output path, risk, or rule is added, update this Markdown file.
6. Commit the Markdown update together with the related code change.

Required first report from every worker:

```text
I read docs/HERMES_WORKER_HANDOFF.md.
Assigned section:
Planned command/work:
Expected output:
Risk checked:
```

Do not accept undocumented work as finished. If the operation changes Hermes behavior, command list, VM role, privacy handling, or output path, it must be reflected in this document.

## 2. VM Roles

### gfield-hq-vm

Purpose:

- Main command center
- Telegram bot
- GitHub sync
- Google Drive scan
- Kakao / report inventory commands
- Algebra2 repository operations

Main path:

```bash
/home/gfield7265/gfield-hq
```

Service:

```bash
gfield-bot.service
```

Common maintenance:

```bash
cd /home/gfield7265/gfield-hq
git pull --ff-only origin main
sudo systemctl restart gfield-bot.service
sudo systemctl status gfield-bot.service --no-pager -l
```

### gfield-core-vm

Purpose:

- Worker server
- Fixed IP tasks
- SMS API / webhook tasks
- Future OCR / report worker
- Future heavy processing

Main path:

```bash
/opt/gfield
```

Rule:

- Do not run Telegram bot here.
- Keep worker/API services separate from the HQ bot.

## 3. Worker Assignments

### A. Overall Command Center Worker

Owner scope:

- `gfield-hq-vm`
- `bot_runner.py`
- `scripts/hq_commands.sh`
- Telegram `/run` command list
- systemd bot status

Primary commands:

```text
/run 상태
/run 목록
/run 동기화
/run 복구
```

English equivalents:

```text
/run status
/run hq_commands
/run deploy_safe
/run hq_rebase
```

Validation:

```bash
cd /home/gfield7265/gfield-hq
git status --short
systemctl is-active gfield-bot.service
systemctl is-enabled gfield-bot.service
```

Report back:

- Latest commit
- Bot active/enabled status
- Whether `/run 목록` displays all Korean commands
- Any command that fails

### B. Report / Kakao Data Worker

Owner scope:

- Google Drive scan output
- Kakao file candidate extraction
- Report material inventory
- No raw private data in GitHub

Primary commands:

```text
/run drive_scan
/run 카톡정리
/run 리포트정리
/run 리포트상태
```

Script paths:

```bash
/home/gfield7265/gfield-hq/scripts/drive_scan.py
/home/gfield7265/gfield-hq/scripts/kakao_inventory.py
/home/gfield7265/gfield-hq/scripts/report_inventory.py
/home/gfield7265/gfield-hq/scripts/report_status.py
```

Output paths:

```bash
/home/gfield7265/gfield_output/drive_inventory/
/home/gfield7265/gfield_output/kakao_inventory/
/home/gfield7265/gfield_output/report_inventory/
```

Validation:

```text
1. Run /run drive_scan
2. Run /run 카톡정리
3. Run /run 리포트정리
4. Run /run 리포트상태
```

Check on VM:

```bash
ls -lt /home/gfield7265/gfield_output/drive_inventory | head
ls -lt /home/gfield7265/gfield_output/kakao_inventory | head
ls -lt /home/gfield7265/gfield_output/report_inventory | head
```

Privacy rule:

- Do not commit generated CSV/JSON outputs to GitHub.
- Do not paste full Kakao conversation content into Telegram.
- Telegram output should show counts, filenames, categories, paths, and short samples only.

Report back:

- Total Drive inventory count
- Kakao candidate count
- Report candidate count
- Latest output file paths
- Any privacy risk found

### C. Algebra2 Worker

Owner scope:

- `docssam1/algebra2`
- Existing Algebra2 patch/check commands
- Keep risky patch commands disabled unless explicitly approved

Primary commands:

```text
/run 알지상태
/run 알지백업
/run 알지검사
/run 알지확인
/run 알지정리
```

English equivalents:

```text
/run algebra2_status
/run algebra2_backup
/run algebra2_test
/run algebra2_diff
/run algebra2_clean
```

Restricted commands:

Do not run these unless explicitly approved by the owner:

```text
/run 정오답패치
/run 오엠알패치
/run 교재패치
```

English equivalents:

```text
/run algebra2_patch_answer_matrix
/run algebra2_patch_omr_layout
/run algebra2_patch_materials
```

Validation:

```text
/run 알지상태
/run 알지확인
```

Report back:

- Current branch
- Local/remote commit
- Dirty files, if any
- Whether restricted commands were avoided

### D. Core VM Worker

Owner scope:

- `gfield-core-vm`
- Worker/API/SMS/OCR future tasks
- No Telegram bot process

Validation:

```bash
hostname
whoami
systemctl is-active gfield-bot.service || true
systemctl is-enabled gfield-bot.service || true
```

Expected:

- `hostname`: `gfield-core-vm`
- `gfield-bot.service`: stopped / disabled

Report back:

- Worker service list
- Fixed IP status
- Whether any Telegram bot process is running

## 4. Current Telegram Command List

```text
[HQ]
/run status
/run deploy
/run deploy_safe
/run hq_status
/run hq_rebase
/run hq_commands

[Drive / Report]
/run drive_scan
/run 카톡정리
/run 리포트정리
/run 리포트상태

[Algebra2]
/run algebra2_status
/run algebra2_backup
/run algebra2_diff
/run algebra2_test
/run algebra2_clean
/run algebra2_patch_omr
/run algebra2_patch_materials
/run algebra2_patch_omr_layout
/run algebra2_patch_answer_matrix

[Algebra2 Korean]
/run 알지상태
/run 알지백업
/run 알지확인
/run 알지검사
/run 알지정리
/run 정오답패치
/run 오엠알패치
/run 교재패치

[Korean aliases]
/run 상태
/run 목록
/run 동기화
/run 복구
/run 카톡정리
/run 리포트정리
/run 리포트상태
```

## 5. Handoff Message to Workers

Use this message when assigning work:

```text
GFIELD Hermes currently uses gfield-hq-vm as the only command center and Telegram bot host.
gfield-core-vm is a worker/API server and must not run the Telegram bot.

This is the GFIELD Hermes new-worker onboarding program.
Please check your assigned section in docs/HERMES_WORKER_HANDOFF.md first.
Run only the commands assigned to your role.
Do not commit student/private output files to GitHub.
Do not paste full Kakao raw content into Telegram or chat.

If your work adds or changes any command, VM role, output path, privacy rule, or risk, update docs/HERMES_WORKER_HANDOFF.md and report that update.

After checking, report:
1. What command you ran
2. Whether it succeeded
3. Output file path, if generated
4. Any error or collision risk
5. Any privacy risk
6. Whether docs/HERMES_WORKER_HANDOFF.md needed an update
```
