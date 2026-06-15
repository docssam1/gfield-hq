# 프리미어 HF — SVG 유사문제 PATCH 워크플로우

> 작성: Claude (관호 지시하에) / 2026.06.15

---

## 워크플로우

```
1. Claude → GFIELD_MEMORY/PATCH_SVG_{typeId}.md 작성 (SVG 코드 조각만)
2. GPT   → GitHub fetch + 해당 조각만 patch + push
3. Claude → GitHub Pages에서 결과 확인만
```

---

## Claude가 작성하는 PATCH.md 형식

```markdown
## 수정 대상
- repo: docssam1/Hyper-Focus-answer-Key
- branch: main

## 작업 1 — SVG 파일 신규 생성
### 파일 경로
premier-hyper-focus/assets/similar/sq-01-1.svg

### 내용 (전체 신규)
<svg width="400" height="300" ...>
  ...
</svg>

## 작업 2 — sq-a.js에 svgUrl 추가
### 파일
premier-hyper-focus/data/sq-a.js

### 전
{ id: "1-A", question: "...", answer: "...", hint1: "...", hint2: "..." }

### 후
{ id: "1-A", question: "...", answer: "...", hint1: "...", hint2: "...", svgUrl: "./assets/similar/sq-01-1.svg" }
```

---

## GPT 지시문

```
GFIELD_MEMORY/PATCH_SVG_{typeId}.md 파일을 읽고
GitHub 저장소 docssam1/Hyper-Focus-answer-Key에서
지정된 파일만 수정 후 커밋해줘.
전체 파일 새로 만들지 말고 조각만 교체할 것.
```

---

## 참고 파일 URL (읽기 전용 — 전체 읽기 금지)

| 파일 | 용도 | URL |
|------|------|-----|
| tutor-scripts.js | scriptSummary 확인 (해당 typeId만) | https://raw.githubusercontent.com/docssam1/Hyper-Focus-answer-Key/main/premier-hyper-focus/data/tutor-scripts.js |
| sq-a.js | typeId 1~17 question 구조 확인 | https://raw.githubusercontent.com/docssam1/Hyper-Focus-answer-Key/main/premier-hyper-focus/data/sq-a.js |
| sq-b.js | typeId 18~34 | https://raw.githubusercontent.com/docssam1/Hyper-Focus-answer-Key/main/premier-hyper-focus/data/sq-b.js |
| sq-c.js | typeId 35~54 | https://raw.githubusercontent.com/docssam1/Hyper-Focus-answer-Key/main/premier-hyper-focus/data/sq-c.js |
| 원본 이미지 | Drive 폴더 ID: 1jMg0m9l7BTSkjgeAo0OJDVH02fi5qpnn | https://drive.google.com/drive/folders/1jMg0m9l7BTSkjgeAo0OJDVH02fi5qpnn |

---

## 토큰 절약 원칙

- Claude는 **해당 typeId 조각만** 확인 — 전체 파일 읽기 금지
- GPT는 **변경 조각만** fetch → patch → push — 전체 파일 새로 쓰기 금지
- Claude는 **결과 확인만** — GitHub Pages URL 열어서 SVG 렌더링 확인

---

## SVG 제작 규칙

1. 원본 이미지 + tutor-scripts.js의 해당 typeId `scriptSummary` 동시 참고
2. sq-a/b/c.js 기존 question 숫자와 **다르게** 변형
3. 유사문제 **2개** 생성 (난이도 동급)
4. SVG 크기: `width="400" height="300"`
5. 색상: **흑백** (인쇄 가능)
6. 한글 포함 시: `font-family="Noto Sans KR, sans-serif"`
7. 파일명: `sq-01-1.svg`, `sq-01-2.svg` (typeId 두 자리)

---

## 우선순위

1차: typeId 1~10 (쌓기나무/도형 기본형)
2차: typeId 11~20
3차: 나머지
