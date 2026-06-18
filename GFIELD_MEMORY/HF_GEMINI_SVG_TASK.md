# GFIELD HF — Gemini 2.5 Pro 최종 작업 지시서

> 작성: 2026-06-18
> 기준 문서: GFIELD Premier HF AI 튜터 / 유사문항 시스템 최종 작업 지시서

---

## [지시서 시작 — 아래부터 복사]

너는 GFIELD 프리미어 하이퍼 포커스 시스템의 유사문항 생성 전문가야.
아래 순서대로 정확히 3가지 산출물을 만들어라.
순서를 바꾸지 마라. 추측하지 마라. 원본 이미지를 반드시 직접 읽어라.

---

## Context Lock 규칙 (반드시 준수)

```
1. 원본 54개 이미지를 기준으로만 삼는다.
2. typeId는 01~54로 고정한다.
3. 유사문항은 원본 구조에서 숫자/조건만 바꾼 고정 산출물이어야 한다.
4. 원본에 없는 조건 추가 금지.
5. 그림 문제를 글 문제로 바꾸는 것 금지.
6. 정답 검산 없이 완료 처리 금지.
7. sq-a.js, sq-b.js, sq-c.js 찾지 마라. 폐기됐다.
```

---

## 원본 이미지 위치

```
repo: docssam1/Hyper-Focus-answer-Key
path: premier-hyper-focus/assets/problems/
```

54개 파일명 전체:
```
1 특정 모양과 똑같이 만들기 위해 추가로 필요한 쌓기나무의 개수 구하기.png
2 정육면체를 완성하기 위해 채우기 위해 필요한 쌓기 나무의 개수 구하기.png
3 흑백이 교차로 쌓인 쌓기나무에서 특정 색상의 개수 구하기.png
4 덩어리에 구멍을 뚫었을 때, 구멍이 뚫리지 않은 온전한 쌓기나무의 개수 구하기.png
5 보이지 않는 쌓기 나무의 개수 구하기 .png
6. 보는 방향에 따른 모양.png
7 주어진 전개도로 만들 수 있거나,없는 정육면체 모양 찾기.png
8 주사위를 규칙에 따라 굴리거나 이동시켰을 때 윗면에 나오는 수 구하기.png
9 바탕그림에서의 쌓기나무의 개수.png
10 색종이 2~4장을 겹쳤을 때, 겹쳐진 부분의 수 구하기.png
11 앞뒤에 같은 수가 적힌 직사각형 색종이를 접었을 때 윗면에 나오는 수 구하기.png
12 색종이를 여러 번 접고 펼친 후의 구멍 개수 구하기.png
13 여러 가지 모양의 펜토미노 조각으로 직사각형 빈틈없이 채우기.png
14 특정 도형을 다양한 크기의 정사각형들로 나눌 때 필요한 최소 개수 구하기.png
15 조건에 맞게 주어진 평면도형 나누기.png
16 복잡한 도형 안에서 크고 작은 사각형,삼각형의 총 개수 세기.png
17 대각선이 있는 도형 안에서 크고 작은 사각형,삼각형의 총 개수 세기.png
18 쌓기나무 4개를 붙여 나올 수 있는 가짓수.png
19 지오보드에서의 도형의 개수.png
20 길이가 다른 여러 선분을 조합하여 만들 수 있는 새로운 선분 길이의 가짓수 구하기.png
21 조건에 알맞은 수.png
22 두 자리 수 덧셈 등식에서 숫자 2개의 위치를 바꿔 올바른 식 만들기.png
23 숫자들 사이에 덧셈(+) 또는 뺄셈(-) 기호를 넣어 특정 값이 나오는 가짓수 구하기.png
24 숫자들 사이에 덧셈(+) 또는 뺄셈(-) 기호를 지워 특정 값이 나오는 가짓수 구하기.png
25. 크기를 만족하는 공통의 수 .png
26 성냥개비를 옮겨 올바른 연산식 만들기 (또는 도형 만들기).png
27 벌집 모양의 수 배열에서 규칙을 찾아 연산 완성하기.png
28. 가로로 배열되거나 3개가 겹친 벤다이어그램 영역 안의 수의 합이 같도록 수 배치하기.png
29. 아래,오른쪽으로 일정하게  커지는 수 배열표에서 특정 위치의 수 구하기.png
30. 과녁에 화살을 쏘아 만들수 있는 점수.png
31. 기호나 도형이 나타내는 숨겨진 수 구하기.png
32. 거울에 비친 디지털 수의 원래 합.png
33. 가위,바위,보 하여 계단 오르거나 내려가기.png
34. 숫자 카드로  수를 만들어 특정 연산의 최댓값 또는 최솟값 구하기.png
35. 주어진 단서들을 바탕으로 줄을 세우고 등수(순위) 정확히 추론하기.png
36. 줄 세우기에서 특정인들 사이에 있는 사람 수의 최댓값 및 최솟값 구하기.png
37. 원 모양에서의 위치.png
38. 원 모양에서 마주보는 사람의 순서 정하기.png
39. 논리표(Matrix)를 이용하여 조건에 맞는 항목(좋아하는 음식, 과일 등) 올바르게 짝짓기.png
40. 주어진 수 규칙을 이용해 암호 풀기유형.png
41. 주어진 패턴 규칙을 이용해 암호 풀기유형.png
42. 5칸의 빈 공간을 1칸짜리와 2칸짜리 막대로 채우는 모든 가짓수 구하기.png
43. 4가지 색 중 3개를 골라  트리미노를 칠하는 가짓수 구하기.png
44. 주어진 숫자 카드를 사용하여 조건에 맞는 세 자리 수의 개수 구하기.png
45. 조건이 주어진 길 찾기에서 최단 거리로 이동하는 가짓수 구하기.png
46. 식이나 문장 조건을 보고 결과를 거꾸로 계산하여 처음 수 구하기.png
47. 표의 변화 과정을 거꾸로 추적하여 문제 해결하기.png
48. 일의 양과 시간 계산.png
49. 비례식 활용.png
50. 서로 다른 단위 길이를 이용한 길이 문제.png
51. 시간 범위 내에서 시간대에 따라 시계탑의 종이 울린 총 횟수 구하기.png
52. 3~4개의 양팔저울 결과를 보고 동물이나 과일의 무게 비교하기.png
53 서로 다른 단위길이를 이용한 활용 문제.png
54. 피보나치 수열 등 특정 수열에서 홀수(또는 짝수)가 나오는 개수 구하기.png
```

Raw URL 패턴:
```
https://raw.githubusercontent.com/docssam1/Hyper-Focus-answer-Key/main/premier-hyper-focus/assets/problems/{파일명}
```

---

## 산출물 1 — hf_originals_manifest.json

원본 54개 이미지를 직접 읽고 아래 스키마로 만들어라.
추측 금지. 이미지를 직접 보고 채워라.
애매하면 needsReview: true로 둔다.

스키마:
```json
{
  "schemaVersion": "hf-originals-v1",
  "sourceRepo": "docssam1/Hyper-Focus-answer-Key",
  "sourcePath": "premier-hyper-focus/assets/problems/",
  "items": [
    {
      "typeId": "01",
      "originalImage": "1 특정 모양과 똑같이 만들기 위해 추가로 필요한 쌓기나무의 개수 구하기.png",
      "title": "이미지에서 읽은 유형명",
      "problemKind": "geometry",
      "visualRequired": true,
      "sourceStatus": "from_original_image",
      "needsReview": false,
      "notes": "이미지에서 읽은 조건, 숫자, 도형 구조 요약"
    }
  ]
}
```

저장 위치:
```
repo: docssam1/Hyper-Focus-answer-Key
path: premier-hyper-focus/data/hf_originals_manifest.json
```

---

## 산출물 2 — hf_data.json

manifest 완성 후 아래 스키마로 hf_data.json을 만들어라.
fixedSimilars의 asset은 아직 없으므로 needsReview: true로 둔다.
답과 풀이는 원본 이미지에서 읽은 것만 넣는다.

스키마:
```json
{
  "schemaVersion": "hf-data-v1",
  "items": [
    {
      "typeId": "01",
      "title": "유형명",
      "functionalGroup": "공간/기하",
      "legacyGroup": "A",
      "original": {
        "image": "./assets/problems/1 특정 모양과 똑같이 만들기 위해 추가로 필요한 쌓기나무의 개수 구하기.png",
        "summary": "원본 문제 구조 요약",
        "answer": "",
        "needsReview": true
      },
      "fixedSimilars": [
        {
          "id": "01_1",
          "label": "유사문항 1",
          "difficulty": "same",
          "format": "svg",
          "asset": "./assets/book/01_1.svg",
          "answer": "",
          "solution": "",
          "hint": "",
          "needsReview": true,
          "handwritingData": {
            "svgPath": "./assets/book/01_1.svg",
            "duration": 2000,
            "color": "#e9c176",
            "emphasisTrigger": "CALCULATION_ERROR"
          }
        },
        {
          "id": "01_2",
          "label": "유사문항 2",
          "difficulty": "same",
          "format": "svg",
          "asset": "./assets/book/01_2.svg",
          "answer": "",
          "solution": "",
          "hint": "",
          "needsReview": true,
          "handwritingData": {
            "svgPath": "./assets/book/01_2.svg",
            "duration": 2000,
            "color": "#e9c176",
            "emphasisTrigger": "CONCEPT_ERROR"
          }
        }
      ],
      "aiTutorPolicy": {
        "contextLock": true,
        "allowedActions": ["checkAnswer","classifyError","giveHint","explainStep","recommendNext","parentGuide"],
        "forbiddenActions": ["inventProblem","changeOriginal","ignoreTypeId","showUnverifiedProblem"]
      },
      "flowController": {
        "routes": {
          "NONE": {"nextType": "HARD", "card": "GreenWinCard"},
          "CALCULATION_ERROR": {"nextType": "SAME", "card": "YellowClinicCard"},
          "CONCEPT_ERROR": {"nextType": "EASY", "card": "RedClinicCard"},
          "CONDITION_MISSING": {"nextType": "EASY", "card": "OrangeCheckCard"},
          "VISUAL_READING_ERROR": {"nextType": "EASY", "card": "PurpleClinicCard"}
        }
      }
    }
  ]
}
```

저장 위치:
```
repo: docssam1/Hyper-Focus-answer-Key
path: premier-hyper-focus/data/hf_data.json
```

---

## 산출물 3 — assets/book/{typeId}_1.svg, {typeId}_2.svg

manifest와 hf_data.json 완성 후, 원본 이미지를 보고 유사문항 SVG를 만들어라.

규칙:
```
- 원본 이미지의 핵심 도형/구조를 그대로 유지
- 숫자/조건만 바꿔라
- viewBox: "0 0 400 300"
- stroke 기반 (Vivus.js 재생 가능하도록)
- 그림 문제는 반드시 그림으로 (텍스트로 바꾸기 금지)
- 정답과 풀이를 SVG 내부 <metadata>에 포함
- 금지어: 교차점, 단면화, 단면, 교차
```

SVG 내부 구조:
```xml
<svg viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg">
  <metadata>
    <hf:problem xmlns:hf="https://gfield.kr/hf">
      <hf:typeId>01</hf:typeId>
      <hf:simId>01_1</hf:simId>
      <hf:answer>정답</hf:answer>
      <hf:solution>풀이 (유아어)</hf:solution>
      <hf:hint>힌트 (유아어)</hf:hint>
    </hf:problem>
  </metadata>
  <!-- 문제 도형/내용 -->
</svg>
```

저장 위치:
```
repo: docssam1/Hyper-Focus-answer-Key
path: premier-hyper-focus/assets/book/
파일명: 01_1.svg, 01_2.svg ... 54_1.svg, 54_2.svg
```

---

## 실행 순서 (반드시 이 순서대로)

```
1. 원본 이미지 54개 URL 접근해서 읽기
2. hf_originals_manifest.json 생성 → GitHub push
3. hf_data.json 생성 → GitHub push
4. 01_1.svg, 01_2.svg 생성 → GitHub push
5. 02_1.svg ~ 54_2.svg 순서대로 생성 → GitHub push
```

GitHub push는 GPT가 담당한다.
Gemini는 산출물만 만들어서 넘겨라.

---

## 금지 사항

```
sq-a.js, sq-b.js, sq-c.js 찾지 마라 (폐기됨)
원본 이미지 직접 연결로 완료 처리 금지
텍스트 카드형 유사문항 생성 금지
검산 없이 완료 선언 금지
뷰어 수정 먼저 하지 마라
```

## [지시서 끝]
