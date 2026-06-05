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
old = """                const totalCorrect = this.omrMarks.filter(x => x === true).length;\n                const totalGraded = this.omrMarks.filter(x => x !== null).length;\n\n                const studentName = this.activeStudent ? this.activeStudent.name : \"학생\";"""
new = """                const totalCorrect = this.omrMarks.filter(x => x === true).length;\n                const totalGraded = this.omrMarks.filter(x => x !== null).length;\n                const accuracy = totalGraded === 0 ? 0 : Math.round((totalCorrect / totalGraded) * 100);\n\n                const studentName = this.activeStudent ? this.activeStudent.name : \"학생\";"""
if new not in s:
    if old not in s:
        raise SystemExit('target not found')
    s = s.replace(old, new, 1)
    p.write_text(s, encoding='utf-8')
PY

git add index.html
git commit -m "Fix OMR report accuracy binding" || true
git push origin main

echo "ALGEBRA2 OMR PATCH DONE"
git log -1 --oneline
