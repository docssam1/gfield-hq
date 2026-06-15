# 프리미어 하이퍼 포커스 — SVG 유사문제 제작 지시서 (Gemini용)

> 작성: Claude (관호 지시하에) / 2026.06.15

---

## 역할
이미지를 분석해서 SVG 코드를 생성하는 작업자다.

---

## STEP 1. 아래 파일 3개를 먼저 읽어라

### 파일 1 — tutor-scripts.js
```
https://raw.githubusercontent.com/docssam1/Hyper-Focus-answer-Key/main/premier-hyper-focus/data/tutor-scripts.js
```
각 typeId별 `scriptSummary` 파악 → SVG 내용의 기준이 된다.

### 파일 2 — sq-a.js
```
https://raw.githubusercontent.com/docssam1/Hyper-Focus-answer-Key/main/premier-hyper-focus/data/sq-a.js
```

### 파일 3 — sq-b.js, sq-c.js
```
https://raw.githubusercontent.com/docssam1/Hyper-Focus-answer-Key/main/premier-hyper-focus/data/sq-b.js
https://raw.githubusercontent.com/docssam1/Hyper-Focus-answer-Key/main/premier-hyper-focus/data/sq-c.js
```
기존 question 텍스트의 숫자/조건 파악 → SVG에서 다른 숫자 사용해야 함.

---

## STEP 2. 원본 이미지 확인 및 분류 검증

**Google Drive 폴더:**
```
폴더 ID: 1jMg0m9l7BTSkjgeAo0OJDVH02fi5qpnn
폴더명: 프리미어 시험유형
```

이 폴더에서 아래 39개 typeId 이미지를 하나씩 열어서 판단:

| 판단 | 기준 |
|------|------|
| ✅ SVG 가능 | 격자/도형/숫자 배열로 재현 가능 |
| ⚠️ 부분 가능 | 텍스트+간단한 도형 조합 |
| ❌ 보류 | 너무 복잡하거나 손그림 수준 |

**검증 대상 typeId (39개):**
```
1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
22, 23, 24, 25, 26, 27, 28, 29, 30, 31,
32, 40, 41, 42, 43, 45, 49, 52, 54
```

**검증 결과 보고 형식:**
```
typeId 1: ✅ SVG 가능 — 격자 3×3 쌓기나무 배치
typeId 2: ✅ SVG 가능 — 3D 큐브 격자
typeId 6: ⚠️ 부분 가능 — 방향 화살표 + 블록
typeId 13: ❌ 보류 — 펜토미노 복잡
...
```

---

## STEP 3. SVG 생성 규칙

1. **원본 이미지** + **tutor-scripts.js의 해당 typeId scriptSummary** 동시 참고
2. **sq-a/b/c.js의 기존 question 숫자와 다르게** 변형
3. 유사문제 **2개** 생성 (난이도 동급)
4. SVG 크기: `width="400" height="300"`
5. 색상: **흑백** (인쇄 가능)
6. 한글 텍스트 포함 시: `font-family="Noto Sans KR, sans-serif"`
7. 파일명: `sq-01-1.svg`, `sq-01-2.svg` (typeId 두 자리)

---

## STEP 4. 결과물 저장 위치

```
repo: docssam1/Hyper-Focus-answer-Key
branch: main
경로: premier-hyper-focus/assets/similar/
파일명 예시:
  sq-01-1.svg  ← typeId 1, 유사문제 1번
  sq-01-2.svg  ← typeId 1, 유사문제 2번
  sq-02-1.svg
  sq-02-2.svg
  ...
```

---

## 우선순위
- 1차: typeId 1~10
- 2차: typeId 11~20
- 3차: 나머지

---

## 절대 금지
- 기존 sq-a/b/c.js의 question과 똑같은 숫자/조건 사용 금지
- tutor-scripts.js 내용과 맞지 않는 SVG 생성 금지
- 이미지를 직접 보지 않고 추측으로 판단 금지
