# 프리미어 하이퍼 포커스 — 유사문제 SVG 작업 지시서

> 작성: Claude (관호 지시하에)  
> 날짜: 2026.06.15  
> 대상: Gemini Vision + GPT

---

## 1. 목적

54개 유형의 유사문제(sq-a/b/c.js)에 이미지/SVG를 연결한다.  
원본 이미지는 Google Drive `프리미어 시험유형` 폴더(ID: `1jMg0m9l7BTSkjgeAo0OJDVH02fi5qpnn`)에 있다.

---

## 2. 반드시 먼저 읽을 파일

작업 전 아래 3개 파일을 반드시 읽고 내용을 파악한 후 시작할 것.

### 2-1. tutor-scripts.js (핵심 스크립트)
```
repo: docssam1/Hyper-Focus-answer-Key
경로: premier-hyper-focus/data/tutor-scripts.js
```

각 typeId별로 다음 필드가 있음:
- `typeTitle` — 유형 제목
- `scriptSummary` — 문제 핵심 요약 ← **SVG 제작 시 이 내용 기준으로 그릴 것**
- `docssamExplanation` — 풀이 설명 ← **유사문제 숫자/조건 변형 시 참고**
- `answer` — 정답
- `hint` — 힌트 ← **유사문제 hint 작성 시 참고**
- `parentTip` — 학부모 팁

### 2-2. sq-a.js (typeId 1~17 유사문제 데이터)
```
repo: docssam1/Hyper-Focus-answer-Key
경로: premier-hyper-focus/data/sq-a.js
```

### 2-3. sq-b.js + sq-c.js (typeId 18~54)
```
경로: premier-hyper-focus/data/sq-b.js
경로: premier-hyper-focus/data/sq-c.js
```

각 question 객체 구조:
```js
{
  id: "1-A",
  question: "문제 텍스트",
  answer: "정답",
  solution: "풀이",
  hint1: "힌트1",
  hint2: "힌트2",
  svgUrl: ""  // ← 이 필드에 SVG 경로 추가 예정
}
```

---

## 3. 분류표

### A. SVG 새로 제작 (39개) — Gemini Vision 담당

원본 이미지를 보고 SVG 코드로 재현. 숫자/조건만 바꿔서 유사문제 2개 생성.  
**tutor-scripts.js의 scriptSummary를 반드시 참고해서 SVG 내용이 맞는지 검증할 것.**

| typeId | 유형명 |
|--------|--------|
| 1 | 쌓기나무 추가 개수 |
| 2 | 큐브 상자 채우기 |
| 3 | 흑백 쌓기나무 |
| 4 | 구멍 뚫린 쌓기나무 |
| 5 | 보이지 않는 쌓기나무 |
| 6 | 보는 방향 모양 |
| 7 | 전개도 정육면체 |
| 8 | 주사위 굴리기 |
| 9 | 바탕그림 쌓기나무 |
| 10 | 색종이 겹치기 |
| 11 | 색종이 접기 숫자 |
| 12 | 색종이 구멍 뚫기 |
| 13 | 펜토미노 채우기 |
| 14 | 정사각형 가장 적게 나누기 |
| 15 | 평면도형 나누기 |
| 16 | 도형 안 사각형 세기 |
| 17 | 대각선 도형 세기 |
| 18 | 쌓기나무 4개 가짓수 |
| 19 | 지오보드 도형 |
| 20 | 선분 길이 조합 |
| 22 | 두 자리 수 덧셈 등식 |
| 23 | 기호 넣어 가짓수 |
| 24 | 기호 지워 가짓수 |
| 25 | 공통의 수 |
| 26 | 성냥개비 연산식 |
| 27 | 벌집 수 배열 |
| 28 | 벤다이어그램 수 배치 |
| 29 | 수 배열표 |
| 30 | 과녁 점수 |
| 31 | 기호/도형 숨겨진 수 |
| 32 | 디지털 수 거울 |
| 40 | 수 규칙 암호 |
| 41 | 패턴 규칙 암호 |
| 42 | 막대로 칸 채우기 |
| 43 | 트리미노 색칠 가짓수 |
| 45 | 최단거리 가짓수 |
| 49 | 비례식 활용 |
| 52 | 양팔저울 무게 비교 |
| 54 | 피보나치 홀짝 |

### B. 텍스트만 (15개) — HTML 텍스트로 처리

숫자/이름만 바꾼 텍스트 문제. 이미지 불필요.  
**tutor-scripts.js의 docssamExplanation 참고해서 숫자/조건 변형할 것.**

21, 33, 34, 35, 36, 37, 38, 39, 44, 46, 47, 48, 50, 51, 53

---

## 4. Gemini Vision 작업 지시

### 4-1. 분류 검증 (먼저 할 것)

Drive 폴더(`1jMg0m9l7BTSkjgeAo0OJDVH02fi5qpnn`)에서 각 이미지를 열고:
- tutor-scripts.js의 해당 typeId `scriptSummary`와 이미지가 일치하는지 확인
- SVG로 재현 가능한가?
- 숫자만 바꿔도 되는가?
- 구조가 복잡해서 보류해야 하는가?

### 4-2. SVG 생성 규칙

1. 원본 이미지 + tutor-scripts.js scriptSummary 동시 참고
2. 숫자/조건만 바꿔서 유사문제 2개 생성
3. SVG 크기: `width="400" height="300"` 기준
4. 색상: 흑백 위주 (인쇄 가능해야 함)
5. 파일명: `sq-{typeId}-1.svg`, `sq-{typeId}-2.svg`
6. sq-a/b/c.js의 기존 question 텍스트와 겹치지 않게 숫자 변형

### 4-3. 결과물 저장 위치

```
GitHub: docssam1/Hyper-Focus-answer-Key
경로: premier-hyper-focus/assets/similar/
파일명: sq-01-1.svg, sq-01-2.svg ... sq-54-1.svg, sq-54-2.svg
```

---

## 5. GPT 작업 지시

Gemini가 생성한 SVG를 GitHub에 push:

```
repo: docssam1/Hyper-Focus-answer-Key
branch: main
경로: premier-hyper-focus/assets/similar/
```

sq-a/b/c.js의 각 question 객체에 `svgUrl` 필드 추가:
```js
svgUrl: "./assets/similar/sq-01-1.svg"
```

---

## 6. 우선순위

1차: typeId 1~10 (쌓기나무/도형 기본형)  
2차: typeId 11~20  
3차: typeId 21~54 나머지

---

## 7. 관련 파일 전체 목록

| 파일 | repo / 위치 |
|------|-------------|
| **tutor-scripts.js** | `Hyper-Focus-answer-Key / premier-hyper-focus/data/tutor-scripts.js` |
| **sq-a.js** | `Hyper-Focus-answer-Key / premier-hyper-focus/data/sq-a.js` |
| **sq-b.js** | `Hyper-Focus-answer-Key / premier-hyper-focus/data/sq-b.js` |
| **sq-c.js** | `Hyper-Focus-answer-Key / premier-hyper-focus/data/sq-c.js` |
| 원본 이미지 | Drive 폴더 `1jMg0m9l7BTSkjgeAo0OJDVH02fi5qpnn` |
| SVG 저장 위치 | `Hyper-Focus-answer-Key / premier-hyper-focus/assets/similar/` |
| 뷰어 | `Hyper-Focus-answer-Key / premier-hyper-focus/viewer-ai-tutor.html` |
