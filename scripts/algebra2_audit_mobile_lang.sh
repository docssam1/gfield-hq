#!/usr/bin/env bash
set -euo pipefail

REPO="$HOME/gfield-projects/algebra2"
cd "$REPO"
git fetch origin main >/dev/null 2>&1 || true
git pull --ff-only origin main >/dev/null

python3 - <<'PY'
from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')
lines = s.splitlines()

print('=== ALGEBRA2 MOBILE + LANGUAGE AUDIT ===')
print()
print('[basic]')
print('viewport:', 'OK' if 'name="viewport"' in s and 'width=device-width' in s else 'MISSING')
print('tailwind:', 'OK' if 'cdn.tailwindcss.com' in s else 'MISSING')
print('chartjs:', 'OK' if 'chart.js' in s else 'MISSING')
print()

# Mobile risk checks
risk_patterns = [
    ('fixed min-width', r'min-w-\[[^\]]+\]'),
    ('horizontal overflow', r'overflow-x-auto'),
    ('large fixed height', r'h-\d+|max-h-\[[^\]]+\]'),
    ('wide grid columns', r'grid-cols-\[|repeat\(20'),
]
print('[mobile risk candidates]')
for label, pat in risk_patterns:
    found = []
    for i, line in enumerate(lines, 1):
        if re.search(pat, line):
            found.append((i, line.strip()[:140]))
    print(f'- {label}: {len(found)}')
    for i, text in found[:12]:
        print(f'  L{i}: {text}')
    if len(found) > 12:
        print(f'  ... +{len(found)-12} more')
print()

# UI Korean fixed text in key tags
print('[language toggle risk: Korean hard-coded UI text]')
tag_re = re.compile(r'<(button|h1|h2|h3|h4|span|p|input|textarea|div|td|th)[^>]*(?:>|$)', re.I)
ko_re = re.compile(r'[가-힣]')
ui_hits = []
for i, line in enumerate(lines, 1):
    if ko_re.search(line) and (tag_re.search(line) or 'placeholder=' in line or 'textContent' in line or 'innerHTML' in line):
        txt = line.strip()
        if len(txt) > 180:
            txt = txt[:180] + '...'
        ui_hits.append((i, txt))
print('hard-coded Korean UI candidates:', len(ui_hits))
for i, txt in ui_hits[:60]:
    print(f'L{i}: {txt}')
if len(ui_hits) > 60:
    print(f'... +{len(ui_hits)-60} more')
print()

# Header/buttons/nav focused checks
print('[header/nav/button focus]')
focus_words = ['성적표', '시험지', '다운로드', '워크북', '해설지', '학생', '등록', '초기화', '평가 가이드', '문제 풀이', 'OMR', '학부모', '로드맵', '전송', '닫기']
for word in focus_words:
    hits = [(i, line.strip()[:140]) for i, line in enumerate(lines,1) if word in line]
    if hits:
        print(f'- {word}: {len(hits)}')
        for i, txt in hits[:5]:
            print(f'  L{i}: {txt}')
print()

# existing language infrastructure
print('[language infrastructure]')
for token in ['currentLanguage', 'isKo', 'setLanguage', 'toggleLanguage', 'data-i18n', 'lang-toggle']:
    print(f'{token}:', s.count(token))
print()

print('[summary]')
print('1. 모바일 기본 viewport는 존재하지만, 상단 버튼/탭/표는 모바일 UX 재정리 필요.')
print('2. 한영 전환 인프라가 부족하거나 부분 적용 상태로 보임.')
print('3. 다음 패치는 먼저 Header/Nav/Top buttons/Student controls를 i18n dictionary 구조로 분리하는 것이 안전.')
print('4. 큰 자동 치환보다 구역별 패치가 안전: header -> nav -> test viewer -> OMR -> report -> roadmap 순서 권장.')
PY
