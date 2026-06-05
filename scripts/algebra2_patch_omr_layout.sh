#!/usr/bin/env bash
set -euo pipefail

REPO="$HOME/gfield-projects/algebra2"
cd "$REPO"
git pull --ff-only origin main

git config user.name "GFIELD VM Bot"
git config user.email "docssam1+gfield-vm-bot@gmail.com"

python3 - <<'PY'
from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

pattern = re.compile(r"            buildOmrRows\(\) \{[\s\S]*?\n            setOmrValue\(id, status\) \{")

new_func = r'''            buildOmrRows() {
                const container = document.getElementById('omr-board-list');
                container.innerHTML = "";
                container.className = "grid grid-cols-1 lg:grid-cols-2 gap-4";

                const difficultyBadge = (difficulty) => {
                    const label = difficulty === 'Basic' ? 'B' : difficulty === 'Core' ? 'C' : 'A';
                    const cls = difficulty === 'Basic'
                        ? 'bg-emerald-50 text-emerald-700 border-emerald-100'
                        : difficulty === 'Core'
                            ? 'bg-amber-50 text-amber-700 border-amber-100'
                            : 'bg-rose-50 text-rose-700 border-rose-100';
                    return `<span class="w-6 text-center border rounded-full text-[10px] font-black ${cls}">${label}</span>`;
                };

                const makeQuestionRow = (i) => {
                    const difficulty = this.getDifficultyByQuestionId(i);
                    const domain = appData.questions[i-1]?.domain || "";
                    return `
                        <div class="flex items-center justify-between gap-2 bg-white border border-stone-200 rounded-xl px-2 py-1.5 shadow-sm" title="${domain}">
                            <div class="flex items-center gap-2 min-w-0">
                                <span class="w-9 text-[11px] font-black text-stone-700">Q${i}</span>
                                ${difficultyBadge(difficulty)}
                            </div>
                            <div class="flex items-center gap-1">
                                <button onclick="app.setOmrValue(${i}, true)" id="omr-btn-correct-${i}" class="w-7 h-7 rounded-lg border border-stone-200 text-[10px] font-black flex items-center justify-center hover:bg-emerald-50 hover:text-emerald-600 transition-all bg-white text-stone-600">O</button>
                                <button onclick="app.setOmrValue(${i}, false)" id="omr-btn-incorrect-${i}" class="w-7 h-7 rounded-lg border border-stone-200 text-[10px] font-black flex items-center justify-center hover:bg-rose-50 hover:text-rose-600 transition-all bg-white text-stone-600">X</button>
                            </div>
                        </div>
                    `;
                };

                const makeBlock = (start, end, title) => {
                    const section = document.createElement('div');
                    section.className = "bg-stone-50 border border-stone-200 rounded-2xl p-3";
                    const rows = [];
                    for (let i = start; i <= end; i++) rows.push(makeQuestionRow(i));
                    section.innerHTML = `
                        <div class="text-xs font-black text-stone-700 mb-2">${title}</div>
                        <div class="grid grid-cols-1 gap-1.5">${rows.join('')}</div>
                    `;
                    container.appendChild(section);
                };

                makeBlock(1, 10, "Part 1 · Q1-Q10");
                makeBlock(11, 20, "Part 1 · Q11-Q20");
                makeBlock(21, 30, "Part 2 · Q21-Q30");
                makeBlock(31, 40, "Part 2 · Q31-Q40");
            },

            setOmrValue(id, status) {'''

s2, count = pattern.subn(new_func, s, count=1)
if count != 1:
    raise SystemExit(f'buildOmrRows replace failed: {count}')

p.write_text(s2, encoding='utf-8')
PY

git add index.html
git commit -m "Convert OMR board to four-card grid layout" || true
git push origin main

echo "ALGEBRA2 OMR GRID PATCH DONE"
git log -1 --oneline
