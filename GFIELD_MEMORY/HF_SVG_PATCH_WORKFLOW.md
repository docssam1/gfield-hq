# 프리미어 HF — 유사문제 이미지 PATCH 워크플로우

> 작성: Claude (관호 지시하에) / 2026.06.15

---

## 확정된 방향

SVG 새로 제작 ❌  
원본 이미지 크롭 → `<img>` 태그로 연결 ✅

```
유사문제 = 텍스트(sq.js 이미 완성) + 원본 이미지 크롭본
```

---

## 워크플로우

```
1. Claude → GFIELD_MEMORY/PATCH_IMG_{typeId}.md 작성 (조각만)
2. GPT    → GitHub fetch + 해당 조각만 patch + push
3. Claude → GitHub Pages에서 결과 확인만
```

---

## PATCH 파일 작성 원칙

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

## 작업 1 — sq-a.js에 imgUrl 추가
### 파일
premier-hyper-focus/data/sq-a.js

### 찾을 블록
{ id: "1-A", question: "...", answer: "...", hint1: "...", hint2: "..." }

### 교체할 블록
{ id: "1-A", question: "...", answer: "...", hint1: "...", hint2: "...", imgUrl: "./assets/similar/sq-01-1.jpg" }
```

---

## 이미지 업로드 방법

Drive 원본 이미지 → 크롭 → GitHub push:

```
repo: docssam1/Hyper-Focus-answer-Key
branch: main
경로: premier-hyper-focus/assets/similar/
파일명: sq-01-1.jpg, sq-01-2.jpg ... sq-54-1.jpg, sq-54-2.jpg
```

원본 이미지 위치:
```
Drive 폴더 ID: 1jMg0m9l7BTSkjgeAo0OJDVH02fi5qpnn
URL: https://drive.google.com/drive/folders/1jMg0m9l7BTSkjgeAo0OJDVH02fi5qpnn
```

---

## 참고 파일 URL (필요한 typeId 조각만 읽을 것)

| 파일 | URL |
|------|-----|
| sq-a.js | https://raw.githubusercontent.com/docssam1/Hyper-Focus-answer-Key/main/premier-hyper-focus/data/sq-a.js |
| sq-b.js | https://raw.githubusercontent.com/docssam1/Hyper-Focus-answer-Key/main/premier-hyper-focus/data/sq-b.js |
| sq-c.js | https://raw.githubusercontent.com/docssam1/Hyper-Focus-answer-Key/main/premier-hyper-focus/data/sq-c.js |

---

## 우선순위

- 1차: typeId 1~10
- 2차: typeId 11~20
- 3차: 나머지

---

## 토큰 절약 원칙

- Claude: 해당 typeId 조각만 확인 — 전체 파일 읽기 금지
- GPT: 조각만 교체 — 전체 파일 새로 쓰기 금지
- Claude: 결과 확인만 — GitHub Pages URL에서 이미지 렌더링 확인
