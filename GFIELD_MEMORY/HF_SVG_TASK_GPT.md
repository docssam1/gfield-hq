# 프리미어 하이퍼 포커스 — SVG 유사문제 제작 지시서 (GPT용)

---

## 역할
너는 이미지를 분석해서 SVG 코드를 생성하고 GitHub에 push하는 작업자다.

---

## 작업 순서

### STEP 1. 아래 파일 3개를 먼저 읽어라

**파일 1 — tutor-scripts.js**
```
repo: docssam1/Hyper-Focus-answer-Key (GitHub MCP)
경로: premier-hyper-focus/data/tutor-scripts.js
```
각 typeId별 `scriptSummary` (문제 핵심 요약) 를 파악한다.  
이것이 SVG 내용의 기준이 된다.

**파일 2 — sq-a.js**
```
경로: premier-hyper-focus/data/sq-a.js
```

**파일 3 — sq-b.js, sq-c.js**
```
경로: premier-hyper-focus/data/sq-b.js
경로: premier-hyper-focus/data/sq-c.js
```
각 유사문제의 기존 question 텍스트를 파악한다.  
SVG에서 사용하는 숫자/조건이 기존 문제와 달라야 한다.

---

### STEP 2. 원본 이미지를 보고 분류 검증

**Drive 폴더 ID:** `1jMg0m9l7BTSkjgeAo0OJDVH02fi5qpnn`  
(Google Drive MCP로 파일 목록 조회 후 각 이미지 확인)

아래 39개 typeId 이미지를 하나씩 열어서 판단:

| 판단 | 기준 |
|------|------|
| ✅ SVG 가능 | 격자/도형/숫자 배열로 재현 가능 |
| ⚠️ 부분 가능 | 텍스트+간단한 도형 조합 |
| ❌ 보류 | 너무 복잡하거나 손그림 수준 |

**검증 대상 typeId:**  
1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,  
22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 40, 41, 42, 43, 45, 49, 52, 54

검증 결과를 먼저 보고한 후 승인 받고 진행.

---

### STEP 3. SVG 생성 규칙

1. **원본 이미지** + **tutor-scripts.js의 scriptSummary** 동시 참고
2. **sq-a/b/c.js의 기존 question 숫자와 다르게** 변형
3. 유사문제 **2개** 생성 (난이도 동급)
4. SVG 크기: `width="400" height="300"`
5. 색상: **흑백** (인쇄 가능)
6. 한글 텍스트 포함 시 `font-family="Noto Sans KR, sans-serif"`
7. 파일명: `sq-01-1.svg`, `sq-01-2.svg` (typeId 두 자리)

---

### STEP 4. GitHub push

**SVG 저장:**
```
repo: docssam1/Hyper-Focus-answer-Key
branch: main
경로: premier-hyper-focus/assets/similar/
파일명: sq-01-1.svg, sq-01-2.svg ... sq-54-1.svg, sq-54-2.svg
```

**sq-a/b/c.js 업데이트:**  
각 question 객체에 `svgUrl` 필드 추가:
```js
// 기존
{ id: "1-A", question: "...", answer: "...", ... }

// 추가 후
{ id: "1-A", question: "...", answer: "...", svgUrl: "./assets/similar/sq-01-1.svg" }
```

**우선순위:**
- 1차: typeId 1~10
- 2차: typeId 11~20
- 3차: 나머지

---

## 절대 금지
- 기존 sq-a/b/c.js의 question과 똑같은 숫자/조건 사용 금지
- tutor-scripts.js 내용과 맞지 않는 SVG 생성 금지
- 추측으로 이미지 내용 판단 금지 (반드시 실제 이미지 확인)
- 승인 없이 GitHub push 금지
- 운영본 파일(viewer-ai-tutor.html 등) 수정 금지
