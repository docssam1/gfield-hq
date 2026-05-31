#!/usr/bin/env bash
set -euo pipefail

REPO="$HOME/gfield-projects/algebra2"
cd "$REPO"
git pull --ff-only origin main

git config user.name "GFIELD VM Bot"
git config user.email "docssam1+gfield-vm-bot@gmail.com"

python3 - <<'PY'
from pathlib import Path
p = Path('index.html')
s = p.read_text(encoding='utf-8')
old = """            downloadMaterialPack(type = 'workbook') {
                const sessions = this.lastGeneratedCurriculum?.length
                    ? this.lastGeneratedCurriculum
                    : this.generateAdaptiveCurriculum(this.getWeakestDomainGroups(3), 10, 120);
                const studentName = (this.activeStudent && this.activeStudent.name) ? this.activeStudent.name : "student";
                const html = this.buildMaterialPackHtml(type, sessions);
                const filename = `${studentName}_${type === 'workbook' ? 'workbook' : 'answer_key'}.html`;
                this.downloadHtmlFile(filename, html);
            },"""
new = """            downloadMaterialPack(type = 'workbook') {
                const requestedSessions = Math.max(4, Math.min(30, Number(document.getElementById('curriculum-session-count')?.value || 10)));
                const requestedMinutes = Math.max(30, Math.min(240, Number(document.getElementById('curriculum-session-minutes')?.value || 120)));
                const sessions = this.lastGeneratedCurriculum?.length
                    ? this.lastGeneratedCurriculum
                    : this.generateAdaptiveCurriculum(this.getWeakestDomainGroups(3), requestedSessions, requestedMinutes);
                const studentName = (this.activeStudent && this.activeStudent.name) ? this.activeStudent.name : "student";
                const html = this.buildMaterialPackHtml(type, sessions);
                const filename = `${studentName}_${type === 'workbook' ? 'workbook' : 'answer_key'}.html`;
                this.downloadHtmlFile(filename, html);
            },"""
if old not in s:
    raise SystemExit('target not found')
s = s.replace(old, new, 1)
p.write_text(s, encoding='utf-8')
PY

git add index.html
git commit -m "Use current roadmap settings for material downloads" || true
git push origin main

echo "ALGEBRA2 MATERIALS PATCH DONE"
git log -1 --oneline
