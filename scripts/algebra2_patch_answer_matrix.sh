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

# 1) 한글 안내문에서 Basic/Core/Advanced 영어 설명을 제거하고 한글 설명으로 통일
s = s.replace(
    "? 'O = 정답, X = 오답, - = 미채점 / B = Basic, C = Core, A = Advanced'",
    "? 'O = 정답, X = 오답, - = 미채점 / B = 기본, C = 핵심, A = 심화'"
)

# 2) 기존에 잘못 중복 삽입된 matrix 호출들을 제거
for token in [
    "                            ${answerMatrixHtmlKo}\n\n",
    "                            ${answerMatrixHtmlEn}\n\n",
]:
    s = s.replace(token, "")

# 3) 한글 리포트 첫 번째 grid 앞에는 한글표 1개만 삽입
ko_marker = """                            <div class=\"grid grid-cols-1 md:grid-cols-2 gap-4 mt-4\">
                                <div class=\"bg-stone-50 border border-stone-200 rounded-xl p-4\">
                                    <h4 class=\"font-bold text-emerald-800 text-xs mb-2 border-b border-emerald-100 pb-1\">🌟 강점 분석 영역 (Mastered)</h4>"""
ko_insert = """                            ${answerMatrixHtmlKo}

                            <div class=\"grid grid-cols-1 md:grid-cols-2 gap-4 mt-4\">
                                <div class=\"bg-stone-50 border border-stone-200 rounded-xl p-4\">
                                    <h4 class=\"font-bold text-emerald-800 text-xs mb-2 border-b border-emerald-100 pb-1\">🌟 강점 분석 영역 (Mastered)</h4>"""
if "${answerMatrixHtmlKo}" not in s:
    if ko_marker not in s:
        raise SystemExit('ko insertion target not found')
    s = s.replace(ko_marker, ko_insert, 1)
else:
    # 혹시 다른 곳에 남아 있으면 일단 위 token 제거 후 다시 삽입됨
    pass

# 4) 영어 리포트 첫 번째 grid 앞에는 영어표 1개만 삽입
# 한글 리포트 grid 다음에 나오는 영어 리포트 grid를 찾아서 두 번째 occurrence에 삽입한다.
needle = """                            <div class=\"grid grid-cols-1 md:grid-cols-2 gap-4 mt-4\">
                                <div class=\"bg-stone-50 border border-stone-200 rounded-xl p-4\">
                                    <h4 class=\"font-bold text-emerald-800 text-xs mb-2 border-b border-emerald-100 pb-1\">🌟 Strong Areas (Mastered)</h4>"""
replacement = """                            ${answerMatrixHtmlEn}

                            <div class=\"grid grid-cols-1 md:grid-cols-2 gap-4 mt-4\">
                                <div class=\"bg-stone-50 border border-stone-200 rounded-xl p-4\">
                                    <h4 class=\"font-bold text-emerald-800 text-xs mb-2 border-b border-emerald-100 pb-1\">🌟 Strong Areas (Mastered)</h4>"""
if "${answerMatrixHtmlEn}" not in s:
    if needle not in s:
        raise SystemExit('en insertion target not found')
    s = s.replace(needle, replacement, 1)

# 5) 최종 안전 점검: 한글/영어 matrix 호출은 각각 1회만 허용
ko_count = s.count('${answerMatrixHtmlKo}')
en_count = s.count('${answerMatrixHtmlEn}')
if ko_count != 1 or en_count != 1:
    raise SystemExit(f'answer matrix placement invalid: ko={ko_count}, en={en_count}')

p.write_text(s, encoding='utf-8')
PY

git add index.html
git commit -m "Fix answer matrix language placement" || true
git push origin main

echo "ALGEBRA2 ANSWER MATRIX LANG FIX DONE"
git log -1 --oneline
