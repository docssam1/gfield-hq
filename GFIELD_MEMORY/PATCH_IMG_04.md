## 수정 대상
- repo: docssam1/Hyper-Focus-answer-Key
- branch: main

---

## 작업 1 — 이미지 업로드

 Drive 원본 파일 ID: 1rLXIiAjUQ-XiMTDL1Jpk90lPCGngV6h0  
파일명: 4 덩어리에 구멍을 뚫었을 때, 구멍이 뚫리지 않은 온전한 쌓기나무의 개수 구하기.png

이 이미지를 크롭해서 아래 두 경로에 저장:
```
premier-hyper-focus/assets/similar/sq-04-1.jpg
premier-hyper-focus/assets/similar/sq-04-2.jpg
```

크롭 기준:
- sq-04-1.jpg: 원본 그대로 (문제 그림 전체)
- sq-04-2.jpg: 숫자/조건만 다른 변형 (구멍 위치나 크기 다르게)

---

## 작업 2 — sq-a.js에 imgUrl 추가

### 파일
premier-hyper-focus/data/sq-a.js

### 찾을 블록
```
      {
        id: "4-A",
        difficulty: "same",
        question: "가로 3칸, 세로 3칸, 높이 3층으로 쌓기나무를 쌓았습니다. 위에서 아래까지 구멍이 2칸 뚫려 있다면, 남은 쌓기나무는 몇 개입니까?",
```

### 교체할 블록
```
      {
        id: "4-A",
        difficulty: "same",
        imgUrl: "./assets/similar/sq-04-1.jpg",
        question: "가로 3칸, 세로 3칸, 높이 3층으로 쌓기나무를 쌓았습니다. 위에서 아래까지 구멍이 2칸 뚫려 있다면, 남은 쌓기나무는 몇 개입니까?",
```

### 찾을 블록
```
      {
        id: "4-B",
        difficulty: "same",
        question: "가로 4칸, 세로 4칸, 높이 2층으로 쌓기나무를 쌓았습니다. 위에서 아래까지 구멍이 3칸 뚫려 있다면, 남은 쌓기나무는 몇 개입니까?",
```

### 교체할 블록
```
      {
        id: "4-B",
        difficulty: "same",
        imgUrl: "./assets/similar/sq-04-2.jpg",
        question: "가로 4칸, 세로 4칸, 높이 2층으로 쌓기나무를 쌓았습니다. 위에서 아래까지 구멍이 3칸 뚫려 있다면, 남은 쌓기나무는 몇 개입니까?",
```

---

## GPT 지시문
```
GFIELD_MEMORY/PATCH_IMG_04.md 파일을 읽고
GitHub 저장소 docssam1/Hyper-Focus-answer-Key에서
지정된 블록만 교체 후 커밋해줘.
전체 파일 새로 만들지 말고 조각만 교체할 것.
```
