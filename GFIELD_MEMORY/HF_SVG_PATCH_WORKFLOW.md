# 프리미어 HF — SVG 유사문제 PATCH 워크플로우

> 작성: Claude (관호 지시하에) / 2026.06.15

---

## 워크플로우

```
1. Claude → GFIELD_MEMORY/PATCH_SVG_{typeId}.md 작성 (SVG 코드 조각만)
2. GPT    → GitHub fetch + 해당 조각만 patch + push
3. Claude → GitHub Pages에서 결과 확인만
```

---

## PATCH 파일 작성 원칙 (GPT / Claude 공통)

```
- 줄 번호로 지시하지 마라
- 파일명, 찾을 기존 블록, 교체할 새 블록만 작성하라
- 직접 수정하지 말고 PATCH_REQUEST만 작성하라
- 전체 파일 새로 쓰기 금지
- 기존 정상 기능 건드리지 말 것
```

---

## PATCH 파일 형식

```markdown
## 수정 대상
- repo: docssam1/Hyper-Focus-answer-Key
- branch: main

## 작업 1 — SVG 파일 신규 생성
### 파일 경로
premier-hyper-focus/assets/similar/sq-01-1.svg

### 내용 (전체 신규)
<svg width="400" height="300" xmlns="http://www.w3.org/2000/svg">
  ...
</svg>

## 작업 2 — sq-a.js에 svgUrl 추가
### 파일
premier-hyper-focus/data/sq-a.js

### 찾을 블록
{ id: "1-A", question: "...", answer: "...", hint1: "...", hint2: "..." }

### 교체할 블록
{ id: "1-A", question: "...", answer: "...", hint1: "...", hint2: "...", svgUrl: "./assets/similar/sq-01-1.svg" }
```

---

## 참고 파일 URL (필요한 typeId 부분만 읽을 것 — 전체 읽기 금지)

| 파일 | URL |
|------|-----|
| tutor-scripts.js | https://raw.githubusercontent.com/docssam1/Hyper-Focus-answer-Key/main/premier-hyper-focus/data/tutor-scripts.js |
| sq-a.js | https://raw.githubusercontent.com/docssam1/Hyper-Focus-answer-Key/main/premier-hyper-focus/data/sq-a.js |
| sq-b.js | https://raw.githubusercontent.com/docssam1/Hyper-Focus-answer-Key/main/premier-hyper-focus/data/sq-b.js |
| sq-c.js | https://raw.githubusercontent.com/docssam1/Hyper-Focus-answer-Key/main/premier-hyper-focus/data/sq-c.js |
| 원본 이미지 | Drive 폴더 ID: 1jMg0m9l7BTSkjgeAo0OJDVH02fi5qpnn |

---

## SVG 제작 규칙

1. 원본 이미지 + 해당 typeId의 `scriptSummary` 동시 참고
2. sq-a/b/c.js 기존 question 숫자와 **다르게** 변형
3. 유사문제 **2개** 생성 (난이도 동급)
4. SVG 크기: `width="400" height="300"`
5. 색상: **흑백** (인쇄 가능)
6. 한글 포함 시: `font-family="Noto Sans KR, sans-serif"`
7. 파일명: `sq-01-1.svg`, `sq-01-2.svg` (typeId 두 자리)

---

## 우선순위

- 1차: typeId 1~10
- 2차: typeId 11~20
- 3차: 나머지

---

## 토큰 절약 원칙

- Claude: 해당 typeId 조각만 확인 — 전체 파일 읽기 금지
- GPT: 조각만 교체 — 전체 파일 새로 쓰기 금지
- Claude: 결과 확인만 — GitHub Pages URL에서 SVG 렌더링만 확인
