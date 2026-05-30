# HERMES_COMMAND_CENTER_PLAN

Last updated: 2026-05-30 KST

## 1. Goal

Build G-FIELD Hermes as the central command system for G-FIELD Gifted Education.
The owner should not need to move between GPT, Gemini, GitHub, Drive, Cloud Console, and local PC repeatedly.

The owner should be able to issue Korean natural-language commands from:

- Telegram Bot
- Hermes Web Dashboard

Hermes routes the work to the correct AI, API, storage, or server.

## 2. Final Concept

Hermes is not one chatbot.
Hermes is the G-FIELD operation OS.

```text
Owner
  ↓
Telegram / Hermes Web Dashboard
  ↓
G-FIELD Hermes Command Center
  ↓
Task Router
  ↓
GPT / Gemini / GitHub / Drive / Sheets / Cloud Run / VM
  ↓
Drive / Sheets / GitHub / Project Memory DB / Logs
  ↓
Telegram reply or Hermes Web result
```

## 3. Role Separation

### Telegram

Fast mobile command remote.

Use cases:

- status check
- run automation
- upload photos/PDFs
- request reports
- request homepage changes
- receive completion alerts

### Hermes Web Dashboard

Full admin control panel.

Use cases:

- project status board
- report queue
- student dashboard
- Drive inventory viewer
- homepage preview
- task logs
- payment/consultation/attendance views

### GPT

Main roles:

- parent-facing report text
- Korean copywriting
- explanation style
- math solution checking
- homepage content
- final editing and quality control

### Gemini

Main roles:

- long PDF analysis
- image understanding
- large document processing
- video/document summarization
- bulk material classification

### GitHub

Main roles:

- code repository
- version history
- homepage/source management
- deployment workflow
- documentation handoff

Student personal data must not be stored in GitHub.

### Google Drive

Main file storage:

- reports
- PDFs
- videos
- student photos
- homework images
- generated files
- homepage assets

### Google Sheets

Operation DB:

- students
- attendance
- consultation
- tuition/payment
- tasks
- report status
- class progress

### VM / VPS

Always-on execution:

- Telegram bot
- n8n, if used
- scheduled jobs
- queue workers
- lightweight automation

### Cloud Run

On-demand/scalable execution:

- webhook APIs
- AI routing API
- Drive scan API
- report generation API
- homepage build/deploy API

## 4. Core Programs to Build

1. G-FIELD learning report system
2. Smart Book Builder
3. Top Class prep system
   - Soma Premier
   - Philz The Classic
   - Thinking Bull
4. PDF/image editing and worksheet generator
5. Homepage management system
6. Consultation and entrance test application system
7. Tuition/payment management system
8. Class video management system
9. Traffic/dismissal guidance system
10. Student attendance/progress dashboard
11. Telegram central command bot
12. GitHub Pages / Cloud Run deployment system
13. Project Memory System

## 5. Immediate Development Order

### Phase 1. Stabilize Command Center

- Keep Telegram bot running on VM systemd
- Add safe commands gradually
- Avoid running duplicate bot instances
- Keep all secrets out of GitHub

### Phase 2. Drive Inventory

- Enable Google Drive API
- Create/use service account
- Share docssam1 Drive folders with service account
- Add `/run drive_scan`
- Export full inventory CSV/JSON

### Phase 3. Report Automation

- Collect report templates
- Collect best previous report examples
- Classify report phrases
- Build report draft generator
- Save outputs to Drive
- Later connect to parent-send flow only after approval

### Phase 4. Homepage Premium Rebuild

- Use real G-FIELD content and performance data
- Remove unnecessary Didimdol/homepage irrelevant content
- Use TOP CLASS prep structure:
  - Soma Premier prep
  - Philz The Classic prep
  - Thinking Bull prep
- Include online mock test and Zoom class pathway
- Use YouTube/intro video style carefully
- Avoid direct purchase/payment/cart wording until commerce registration is ready

### Phase 5. Project Memory System

- Store project status
- Store decisions
- Store next actions
- Store source references
- Allow queries like: "homepage where did we stop?"

### Phase 6. Hermes Web Dashboard

- Build admin web dashboard after Telegram command layer is stable
- Show tasks, logs, report queue, Drive scan results, homepage status

## 6. Command Design

Current command:

- `/run status`

Near-term commands:

- `/run deploy`
- `/run drive_scan`
- `/run report_inventory`
- `/run kakao_analyze`
- `/run homepage_build`
- `/run memory_status`

Command rule:

- Korean natural-language command should eventually map to these internal commands.
- Telegram should feel like a Korean remote controller, not a developer console.

## 7. Korean-First Requirement

The owner will operate mostly in Korean.
Hermes must accept Korean commands such as:

- "홈페이지 어디까지 했어?"
- "채원이 리포트 만들어줘"
- "Drive 전체 스캔해"
- "오늘 작업 상태 알려줘"
- "황소 대비 페이지 다시 만들어"

The internal code may be English, but the control layer must be Korean-friendly.

## 8. Local PC and Kakao Strategy

Google Drive and uploaded Kakao logs can be processed from VM/API.
Local PC is only needed when files remain only on the PC or Kakao PC.

Final target:

- important Kakao logs/files should be exported into Drive
- VM scans Drive, not the local PC
- PC should not be required for 24-hour operation

## 9. Credit and Server Strategy

### Initial Period

Use GCP credits aggressively for speed:

- VM
- Cloud Run
- Drive API
- Gemini/Vertex/GenAI services
- Vision/API processing when useful

### Observed Credit Context

- Free Trial credit observed: about KRW 442,623
- GenAI/App Builder credit observed: about KRW 1,475,511
- Exact expiration and eligible services must be checked in Billing.

### 3-Month Strategy

- Use credits to build quickly
- Avoid wasting time over-optimizing too early
- Build working pipelines first

### 1-Year / Long-Term Strategy

- Keep always-on Telegram/n8n/jobs on VM or cheaper VPS
- Keep Cloud Run for scalable/on-demand APIs
- Move stable workloads to cheaper server if needed
- Keep GitHub as permanent code/history source

## 10. Migration Strategy

Hermes must be portable.

If moving to another server:

1. Clone GitHub repo
2. Copy `.env` secrets separately
3. Install Python dependencies
4. Register systemd service
5. Reconnect Drive service account
6. Run `/run status`

Never depend on one chat room as the only memory.

## 11. Security Rules

- Never commit Telegram bot token
- Never commit service account JSON
- Never commit student DB or private photos
- Store secrets in `.env`, Secret Manager, or GitHub Secrets
- GitHub is for code/docs only
- Drive/Sheets are for private operation data

## 12. Success Definition

Hermes succeeds when the owner can say in Korean:

- "오늘 리포트 전체 만들어"
- "홈페이지 최신 버전 반영해"
- "Drive 자료 분류해"
- "지난 작업 어디까지 했지?"

and Hermes routes the job, stores outputs, and reports back without the owner jumping between many tools.

Final sentence:

The owner speaks to Telegram or Hermes Web; GPT, Gemini, Drive, Sheets, GitHub, Cloud Run, and VM move behind the scenes.
