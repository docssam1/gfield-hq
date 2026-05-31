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

insert_after = """                const lowDiffHtmlEn = lowDifficultyWrong.length > 0
                    ? `<div class=\"bg-amber-50 border border-amber-200 rounded-xl p-4 mt-4\">
                        <h4 class=\"font-bold text-amber-900 text-xs mb-2\">⚠️ Low-Difficulty Miss Alert</h4>
                        <ul class=\"list-disc pl-4 text-xs space-y-1 text-stone-700\">
                            ${lowDifficultyWrong.map(x => `<li>Q${x.qId} · ${x.domain}</li>`).join('')}
                        </ul>
                        <p class=\"text-[11px] text-amber-900/80 mt-2\">Repeated misses on easier items often indicate prerequisite gaps before Algebra 2 content.</p>
                    </div>`
                    : '';"""

matrix_block = r'''

                const buildAnswerMatrixHtml = (lang = 'ko') => {
                    const resultLabel = lang === 'ko' ? '결과' : 'Result';
                    const difficultyLabel = lang === 'ko' ? '난이도' : 'Level';
                    const title = lang === 'ko' ? '1~40번 정오답 · 난이도 확인표' : 'Q1-Q40 Answer & Difficulty Matrix';
                    const guide = lang === 'ko'
                        ? 'O = 정답, X = 오답, - = 미채점 / B = Basic, C = Core, A = Advanced'
                        : 'O = Correct, X = Incorrect, - = Ungraded / B = Basic, C = Core, A = Advanced';

                    const makeCell = (qId, type) => {
                        const status = this.omrMarks[qId - 1];
                        const difficulty = this.getDifficultyByQuestionId(qId);
                        if (type === 'number') return `<div class="text-[10px] font-black text-stone-600 text-center">${qId}</div>`;
                        if (type === 'result') {
                            const label = status === true ? 'O' : status === false ? 'X' : '-';
                            const cls = status === true
                                ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                                : status === false
                                    ? 'bg-rose-50 text-rose-700 border-rose-200'
                                    : 'bg-stone-50 text-stone-400 border-stone-200';
                            return `<div class="rounded-md border ${cls} text-[10px] font-black py-1 text-center">${label}</div>`;
                        }
                        const label = difficulty === 'Basic' ? 'B' : difficulty === 'Core' ? 'C' : 'A';
                        const cls = difficulty === 'Basic'
                            ? 'bg-emerald-50 text-emerald-700 border-emerald-100'
                            : difficulty === 'Core'
                                ? 'bg-amber-50 text-amber-700 border-amber-100'
                                : 'bg-rose-50 text-rose-700 border-rose-100';
                        return `<div class="rounded-md border ${cls} text-[10px] font-black py-1 text-center">${label}</div>`;
                    };

                    const makeBand = (start, end, label) => {
                        const nums = [];
                        const results = [];
                        const levels = [];
                        for (let i = start; i <= end; i++) {
                            nums.push(makeCell(i, 'number'));
                            results.push(makeCell(i, 'result'));
                            levels.push(makeCell(i, 'difficulty'));
                        }
                        return `
                            <div class="bg-white border border-stone-200 rounded-xl p-3 overflow-x-auto">
                                <div class="text-[11px] font-black text-stone-700 mb-2">${label}</div>
                                <div class="grid grid-cols-[46px_repeat(20,minmax(28px,1fr))] gap-1 min-w-[720px]">
                                    <div></div>${nums.join('')}
                                    <div class="text-[10px] font-bold text-stone-500 flex items-center">${resultLabel}</div>${results.join('')}
                                    <div class="text-[10px] font-bold text-stone-500 flex items-center">${difficultyLabel}</div>${levels.join('')}
                                </div>
                            </div>
                        `;
                    };

                    return `
                        <div class="bg-stone-50 border border-stone-200 rounded-xl p-4 mt-4">
                            <h4 class="font-bold text-stone-800 text-xs mb-1">${title}</h4>
                            <p class="text-[11px] text-stone-500 mb-3">${guide}</p>
                            <div class="space-y-3">
                                ${makeBand(1, 20, 'Q1-Q20')}
                                ${makeBand(21, 40, 'Q21-Q40')}
                            </div>
                        </div>
                    `;
                };

                const answerMatrixHtmlKo = buildAnswerMatrixHtml('ko');
                const answerMatrixHtmlEn = buildAnswerMatrixHtml('en');
'''

if 'const buildAnswerMatrixHtml' not in s:
    if insert_after not in s:
        raise SystemExit('answer matrix insert target not found')
    s = s.replace(insert_after, insert_after + matrix_block, 1)

s = s.replace("""                            <div class=\"grid grid-cols-1 md:grid-cols-2 gap-4 mt-4\">""", """                            ${answerMatrixHtmlKo}

                            <div class=\"grid grid-cols-1 md:grid-cols-2 gap-4 mt-4\">""", 1)

s = s.replace("""                            <div class=\"grid grid-cols-1 md:grid-cols-2 gap-4 mt-4\">""", """                            ${answerMatrixHtmlEn}

                            <div class=\"grid grid-cols-1 md:grid-cols-2 gap-4 mt-4\">""", 1)

p.write_text(s, encoding='utf-8')
PY

git add index.html
git commit -m "Add answer difficulty matrix to diagnostic report" || true
git push origin main

echo "ALGEBRA2 ANSWER MATRIX PATCH DONE"
git log -1 --oneline
