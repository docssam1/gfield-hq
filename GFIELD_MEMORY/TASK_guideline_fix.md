# TASK: 사고력 진도 기준선(빨간 점선) 위치 버그 수정

## 증상
roadmap/index.html에서 "사고력 진도 기준선"(빨간 점선)이 실제 현재월과 다른 위치에 표시됨.
예: 7세 6월(현재)인데 화면엔 4월쯤에 선이 찍힘.

## 원인
`drawGuideOverlay` 함수가 "첫 번째 월 칸의 폭(width)"을 모든 27개 월 칸에 동일하게 적용된다고 가정하고
픽셀 위치 = 시작점 + (인덱스 × 첫칸폭) 으로 계산합니다.
그런데 표는 `table-layout:fixed`가 아니라서 칸마다 내용 길이에 따라 실제 폭이 달라지고,
인덱스가 클수록(뒤로 갈수록) 오차가 누적되어 위치가 어긋남.

## 해결
첫 칸 폭으로 추정하는 대신, **그 달에 해당하는 실제 th 요소의 화면 위치를 직접 측정**하도록 변경.

## 대상 파일 (repo: docssam1/lete-on)
- `roadmap/index.html`

## 수정 내용 — drawGuideOverlay 함수 내부 (정확히 아래 블록을 통째로 교체)

**찾을 코드 (old):**
```js
  // 현재월의 표시 칸 위치 (사고력1 현재과정 중앙이 여기 옴)
  const nowIdx = toIdx(studentNowMonth(diagData.age)); // 칸 인덱스
  const cellX = nowIdx + 0.5; // 칸 중앙
  const table=document.getElementById('map');
  const monthThs=table.querySelectorAll('#thead .month-head');
  if(!monthThs.length) return;
  const first=monthThs[0].getBoundingClientRect();
  const cw=first.width;
  const tableRect=table.getBoundingClientRect();
  const xPx=(first.left - tableRect.left) + cellX*cw;
  if(xPx<=0 || cw<=0) return; // 레이아웃 미완성 시 스킵
```

**바꿀 코드 (new):**
```js
  // 현재월의 표시 칸 위치 (사고력1 현재과정 중앙이 여기 옴)
  const nowIdx = toIdx(studentNowMonth(diagData.age)); // 칸 인덱스
  const table=document.getElementById('map');
  const monthThs=table.querySelectorAll('#thead .month-head');
  if(!monthThs.length) return;
  // 칸 폭이 들쭉날쭉(table-layout:auto)해도 정확하도록, 균일폭 추정 대신
  // 실제 해당 월 th의 화면 위치를 직접 측정한다.
  const idx=Math.max(0, Math.min(monthThs.length-1, nowIdx));
  const target=monthThs[idx];
  if(!target) return;
  const tr=target.getBoundingClientRect();
  const tableRect=table.getBoundingClientRect();
  const xPx=(tr.left+tr.right)/2 - tableRect.left; // 해당 월 칸의 실제 중앙
  if(xPx<=0) return; // 레이아웃 미완성 시 스킵
```

(앞뒤 줄 `let _lastGuideCur=null; function drawGuideOverlay(cur){...}`의 나머지 부분은 그대로 둠 — 위 블록만 교체)

## 작업 방법
1. GitHub에서 `roadmap/index.html` fetch
2. 위 old 블록을 찾아 new 블록으로 **정확히 교체** (다른 곳 건드리지 말 것)
3. JS 문법 확인 (중괄호·세미콜론 정상인지)
4. push (커밋: `fix(guide-line): 사고력 진도 기준선 위치 계산을 실제 칸 위치 측정 방식으로 수정`)

## 주의
- 파일 전체를 다시 만들지 말 것. 이 블록만 정확히 치환.
- 치환 전 old 블록이 파일에 **정확히 1곳**만 있는지 확인 후 교체.
