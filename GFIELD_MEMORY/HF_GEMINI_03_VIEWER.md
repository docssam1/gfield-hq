# HF 작업 지시서 03 — viewer_handwriting.js 작성

> Gemini 2.5 Pro AI Studio에 아래 내용을 그대로 붙여넣을 것
> 반드시 02_DATA 작업 완료 후 진행

---

## [지시서 시작]

너는 GFIELD 프리미어 하이퍼 포커스 뷰어의 프론트엔드 개발자야.
hf_data.json의 handwritingData를 받아서 Vivus.js와 Khoshnus.js로
손글씨 애니메이션을 재생하는 연동 코드를 작성해줘.

---

## STEP 1. 읽어야 할 파일

### hf_data.json (방금 생성된 것)
```
https://raw.githubusercontent.com/docssam1/Hyper-Focus-answer-Key/main/premier-hyper-focus/data/hf_data.json
```

### 아키텍처 설계도
```
https://raw.githubusercontent.com/docssam1/gfield-hq/main/GFIELD_MEMORY/HF_ARCHITECTURE.md
```

---

## STEP 2. 작업 목적

```
hf_data.json의 handwritingData
  ↓
viewer_handwriting.js가 읽어서
  ↓
Vivus.js → 도형/격자 SVG Path 애니메이션
Khoshnus.js → 수식 텍스트 손글씨 애니메이션
  ↓
viewer-ai-tutor.html에서 재생
```

---

## STEP 3. HTML에 필요한 것 (viewer에 추가할 태그)

```html
<!-- CDN -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/vivus/0.4.6/vivus.min.js"></script>

<!-- 손글씨 도형 영역 -->
<svg id="handwriting-svg" viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg">
  <path id="handwriting-path" d="" stroke="#FF0000" stroke-width="2" fill="none"/>
</svg>

<!-- 손글씨 수식 영역 -->
<svg id="math-handwriting-svg" viewBox="0 0 400 100" xmlns="http://www.w3.org/2000/svg"></svg>
```

---

## STEP 4. 작성할 코드 규칙

### 핵심 함수 3개

**1. playHandwriting(handwritingData)**
- hf_data.json의 handwritingData를 받아서 Vivus.js로 재생
- svgPath를 `#handwriting-path`에 주입
- duration, color 적용
- Vivus type: `delayed` (손글씨 느낌 최적)

**2. playMathHandwriting(formulaText)**
- 수식 텍스트(예: 27-5=22)를 Khoshnus.js로 글자별 손글씨 재생
- eachLetterDelay: 200ms

**3. handleEmphasis(emphasisTrigger)**
- CALCULATION_ERROR: stroke-width 4, 빨간색 강조
- CONCEPT_ERROR: stroke-width 3, 파란색 강조
- NONE: 기본값

### lockPolicy 연동
- LV1: fixedSimilars 2개에만 손글씨 재생
- LV2: 전체 재생
- userLevel 파라미터로 제어

### 오류 처리
- handwritingData가 null이면 손글씨 영역 숨김
- Vivus 로드 실패시 graceful fallback (텍스트만 표시)

---

## 출력 규칙
- JavaScript 파일만 출력
- ES6 모듈 형식
- 파일명: `viewer_handwriting.js`

## [지시서 끝]

완성 후 GitHub에 올려줘:
```
repo: docssam1/Hyper-Focus-answer-Key
branch: main
경로: premier-hyper-focus/data/viewer_handwriting.js
```
