# HF 작업 지시서 02 — hf_data.json 생성 (54개 전체)

> Gemini 2.5 Pro AI Studio에 아래 내용을 그대로 붙여넣을 것
> 반드시 01_RUNTIME 작업 완료 후 진행

---

## [지시서 시작]

너는 GFIELD 프리미어 하이퍼 포커스 AI 튜터 시스템의 데이터 생성자야.
아래 파일들을 읽고 54개 유형 전체 JSON 데이터를 만들어줘.

---

## STEP 1. 아래 파일 전부 읽기

### tutor-scripts.js (54개 유형 핵심 데이터)
```
https://raw.githubusercontent.com/docssam1/Hyper-Focus-answer-Key/main/premier-hyper-focus/data/tutor-scripts.js
```

### 유사문제 데이터
```
https://raw.githubusercontent.com/docssam1/Hyper-Focus-answer-Key/main/premier-hyper-focus/data/sq-a.js
https://raw.githubusercontent.com/docssam1/Hyper-Focus-answer-Key/main/premier-hyper-focus/data/sq-b.js
https://raw.githubusercontent.com/docssam1/Hyper-Focus-answer-Key/main/premier-hyper-focus/data/sq-c.js
```

### 아키텍처 설계도
```
https://raw.githubusercontent.com/docssam1/gfield-hq/main/GFIELD_MEMORY/HF_ARCHITECTURE.md
```

---

## STEP 2. 스키마 (typeId별 구조)

```json
{
  "typeId": 1,
  "legacyGroup": "A",
  "functionalGroup": "공간/기하",
  "title": "쌓기나무 앞/뒤에서 본 모양으로 개수 구하기",
  "targetUser": {
    "profile": "수학 앞서가는 7세",
    "mathReadyLevel": ["초2 주력", "초3 연산 허용"]
  },
  "languagePolicy": {
    "voice": "따뜻한 유아어",
    "blockedWords": ["교차점", "단면화", "단면", "교차"],
    "preferredPhrases": ["대장 블록", "케이크 쪼개기", "콕콕 세기"]
  },
  "originalProblem": {
    "questionId": "q01_origin",
    "difficulty": "same",
    "text": "문제 텍스트",
    "answer": "정답",
    "answerStory": "풀이 스토리 (유아어)",
    "audioPath": null
  },
  "fixedSimilars": [
    {
      "questionId": "q01_easy_1",
      "difficulty": "easy",
      "text": "문제 텍스트",
      "answer": "정답",
      "answerStory": "풀이 스토리 (유아어)",
      "handwritingData": {
        "svgPath": "사람이 쓴 듯한 자연스러운 Bezier 곡선 SVG Path 문자열",
        "duration": 2000,
        "color": "#FF0000",
        "emphasisTrigger": "CALCULATION_ERROR"
      },
      "audioPath": null,
      "audioScript": "[도입] → [핵심 개념 1문장] → [실수 방지 팁] → [격려] 30초 이내"
    },
    {
      "questionId": "q01_same_1",
      "difficulty": "same",
      "text": "문제 텍스트",
      "answer": "정답",
      "answerStory": "풀이 스토리 (유아어)",
      "handwritingData": {
        "svgPath": "SVG Path 문자열",
        "duration": 2000,
        "color": "#0000FF",
        "emphasisTrigger": "CONCEPT_ERROR"
      },
      "audioPath": null,
      "audioScript": "[도입] → [핵심 개념 1문장] → [실수 방지 팁] → [격려] 30초 이내"
    }
  ],
  "aiTutorPack": {
    "conceptAudioPath": null,
    "audioScript": "독쌤 음성 스크립트 30초 이내",
    "problemPool": {
      "easy": [],
      "same": [],
      "hard": []
    }
  },
  "flowController": {
    "routes": {
      "CALCULATION_ERROR": {
        "recommendedDifficulty": "SAME",
        "feedbackTitle": "아까운 계산 실수!",
        "feedbackText": "칭찬 샌드위치 형식 피드백 (유아어)",
        "stitchesCard": "YellowClinicCard",
        "showRetryButton": true,
        "showAudioPlayer": false,
        "conceptAudioPath": null
      },
      "CONCEPT_ERROR": {
        "recommendedDifficulty": "EASY",
        "feedbackTitle": "개념 콕콕 클리닉",
        "feedbackText": "칭찬 샌드위치 형식 피드백 (유아어)",
        "stitchesCard": "RedClinicCard",
        "showRetryButton": true,
        "showAudioPlayer": true,
        "conceptAudioPath": null
      },
      "NONE": {
        "recommendedDifficulty": "HARD",
        "feedbackTitle": "정답 반짝 카드",
        "feedbackText": "격려 메시지 (유아어)",
        "stitchesCard": "GreenWinCard",
        "showRetryButton": false,
        "showAudioPlayer": false,
        "conceptAudioPath": null
      }
    }
  },
  "adPolicy": {
    "lv1BannerEnabled": true,
    "lv1InterstitialTriggers": ["tutorLimitReached", "pdfExport"]
  }
}
```

---

## STEP 3. 생성 원칙

- tutor-scripts.js의 `scriptSummary`, `docssamExplanation`, `hint`, `parentTip` 반드시 참고
- sq-a/b/c.js의 기존 question 텍스트와 **다른** 숫자/조건 사용
- 모든 텍스트에서 금지어(교차, 단면 등) 사용 금지
- 유아어 우선: '교차점' → '길이 만나는 곳', '단면' → '잘린 면'
- handwritingData.svgPath: **반드시 Bezier 곡선(C, Q 명령어 포함)으로 자연스럽게 생성**
- audioScript: [도입] → [핵심 개념 1문장] → [실수 방지 팁] → [격려] 30초 이내
- 칭찬 샌드위치: 잘한 점 → 수정할 점 → 격려 순서

### legacyGroup / functionalGroup 매핑
| legacyGroup | typeId |
|---|---|
| A (그림 위주) | 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,22,23,24,25,26,27,28,29,30,31,32,40,41,42,43,45,49,52,54 |
| B (텍스트 위주) | 21,33,34,35,36,37,38,39,44,46,47,48,50,51,53 |

| functionalGroup | typeId |
|---|---|
| 공간/기하 | 1,2,3,4,5,6,7,8,9,10 |
| 평면/논리 | 11,12,13,14,15,16,17,18,19,32,33,34,35,36,37,38,39 |
| 연산/규칙 | 20,21,22,23,24,25,26,27,28,29,30,31,40,41,42,43,44 |
| 가중치/활용 | 45,46,47,48,49,50,51,52,53,54 |

---

## 출력 규칙
- JSON만 출력 (다른 텍스트 없이)
- 54개 전체를 배열로
- 파일명: `hf_data.json`

## [지시서 끝]

완성 후 GitHub에 올려줘:
```
repo: docssam1/Hyper-Focus-answer-Key
branch: main
경로: premier-hyper-focus/data/hf_data.json
```
