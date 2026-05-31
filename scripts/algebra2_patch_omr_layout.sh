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
                container.className = "space-y-4";

                const makeQuestionCell = (i) => {
                    const difficulty = this.getDifficultyByQuestionId(i);
                    const domain = appData.questions[i-1]?.domain || "";
                    return `
                        <div class="min-w-[74px] bg-white border border-stone-200 rounded-xl p-2 flex flex-col items-center gap-1 shadow-sm hover:bg-stone-50 transition-all" title="${domain}">
                            <div class="text-[10px] font-black text-stone-700">Q${i}</div>
                            <div class="text-[9px] font-bold rounded-full px-2 py-0.5 ${difficulty === 'Basic' ? 'bg-emerald-50 text-emerald-700' : difficulty === 'Core' ? 'bg-amber-50 text-amber-700' : 'bg-rose-50 text-rose-700'}">${difficulty === 'Basic' ? 'B' : difficulty === 'Core' ? 'C' : 'A'}</div>
                            <div class="flex items-center gap-1 mt-1">
                                <button onclick="app.setOmrValue(${i}, true)" id="omr-btn-correct-${i}" class="w-7 h-7 rounded-lg border border-stone-200 text-[10px] font-black flex items-center justify-center hover:bg-emerald-50 hover:text-emerald-600 transition-all bg-white text-stone-600">O</button>
                                <button onclick="app.setOmrValue(${i}, false)" id="omr-btn-incorrect-${i}" class="w-7 h-7 rounded-lg border border-stone-200 text-[10px] font-black flex items-center justify-center hover:bg-rose-50 hover:text-rose-600 transition-all bg-white text-stone-600">X</button>
                            </div>
                        </div>
                    `;
                };

                const makeRow = (start, end, title) => {
                    const section = document.createElement('div');
                    section.className = "bg-stone-50 border border-stone-200 rounded-2xl p-3";
                    const cells = [];
                    for (let i = start; i <= end; i++) cells.push(makeQuestionCell(i));
                    section.innerHTML = `
                        <div class="text-xs font-black text-stone-700 mb-2">${title}</div>
                        <div class="flex gap-2 overflow-x-auto pb-1">${cells.join('')}</div>
                    `;
                    container.appendChild(section);
                };

                makeRow(1, 20, "Part 1 · Q1-Q20");
                makeRow(21, 40, "Part 2 · Q21-Q40");
            }

            setOmrValue(id, status) {'''

s2, count = pattern.subn(new_func, s, count=1)
if count != 1:
    raise SystemExit(f'buildOmrRows replace failed: {count}')

p.write_text(s2, encoding='utf-8')
PY

git add index.html
git commit -m "Convert OMR board to two-row horizontal layout" || true
git push origin main

echo "ALGEBRA2 OMR LAYOUT PATCH DONE"
git log -1 --oneline
