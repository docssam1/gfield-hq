# TASK: roadmap/index.html 진단결과 화면 수정

## 배경
현재 roadmap/index.html(GitHub 최신)에서 진단 완료 후 결과 화면에
코멘트(상담 문구)와 그래프가 정상 표시되지 않는 문제가 있음.
demo/index.html과 비교해 누락된 요소를 파악하고 수정.

## 확인된 차이 (Claude 분석 완료)

**roadmap에 없고 demo에 있는 것:**
1. **인쇄 버튼** (`print-btn-wrap` 블록) — studentComment div 바로 아래에 있어야 함

demo의 인쇄 버튼 블록 (정확히 이 내용):
```html
  <div class="print-btn-wrap" style="text-align:center;margin:18px 0 4px">
    <button class="print-btn" onclick="printRoadmap()" style="display:inline-flex;align-items:center;gap:8px;padding:13px 26px;border:0;border-radius:9px;background:#1a2740;color:#fff;font-size:15px;font-weight:800;cursor:pointer;letter-spacing:.01em">
      <span style="font-size:17px">🖨</span> 로드맵 분석 PDF로 저장 / 인쇄
    </button>
    <div style="font-size:11px;color:#94a3b8;margin-top:8px">가로 방향으로 인쇄됩니다. 인쇄 창에서 '대상'을 <b>PDF로 저장</b>으로 선택하세요.</div>
  </div>
```

2. **인쇄용 CSS** (`@media print` 블록) — demo에는 있고 roadmap에는 없거나 누락됨

## 작업 방법

### Step 1: 현재 상태 파악
1. GitHub에서 `roadmap/index.html` fetch
2. `studentComment` div 바로 다음에 `print-btn-wrap`이 있는지 확인
3. `@media print` 블록이 있는지 확인
4. `fillComment` 함수와 `progressGraphWrap` 이 있는지 확인

### Step 2: demo와 비교해서 누락 요소 파악
- demo(`roadmap/demo/index.html`)도 fetch해서 섹션별 비교
- `studentResult` 섹션 내부 구조가 일치하는지 확인

### Step 3: roadmap에 누락 요소 추가
- `<div class="comment" id="studentComment"></div>` 바로 뒤에 인쇄 버튼 블록 삽입
- `@media print` CSS가 없으면 demo에서 복사해서 추가
- `printRoadmap` 함수가 없으면 demo에서 복사해서 추가

### Step 4: push
- 커밋: `fix(roadmap): 진단결과 화면 인쇄버튼+CSS 복구 (demo 기준)`
- 파일: `roadmap/index.html`

## 주의사항
- 전체 파일 재작성 금지 — 누락된 부분만 추가
- demo 고유 요소(워터마크, 보안 스크립트 등)는 roadmap에 넣지 말 것
- L3·L4 행, 연산 통일, 동적 그래프 등 기존 수정 내용 건드리지 말 것
- push 전 JS 문법 오류 없는지 확인

## 추가 확인 사항
원장님 말씀: "표만 있고 그래프 아래 문구(코멘트)가 없다"
→ `fillComment` 함수 자체는 두 파일 모두에 있음
→ 혹시 `drawProgressGraph` 호출 후 `fillComment`가 호출되지 않거나
  `studentResult` 섹션이 `display:block`으로 안 바뀌는 게 원인일 수 있음
→ 진단 제출 후 결과 표시 흐름(`fillLevelDelta → fillComment → drawProgressGraph → studentResult.display=block`)이
  roadmap과 demo에서 동일한지 확인 후 다르면 맞춰줄 것
