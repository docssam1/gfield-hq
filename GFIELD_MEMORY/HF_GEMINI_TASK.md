# GFIELD HF — Gemini 2.5 Pro 작업 지시서

> AI Studio (gemini-2.5-pro) 에 아래 내용을 그대로 붙여넣을 것

---

## [지시서 시작 — 아래부터 복사]

너는 GFIELD 프리미어 하이퍼 포커스 AI 튜터 시스템의 백엔드 개발자야.
아래 기존 코드와 설계도를 읽고 세 가지 결과물을 만들어줘.

---

## 읽어야 할 파일 (전부 읽을 것)

### 1. 기존 런타임 (type4 기준)
```
https://raw.githubusercontent.com/docssam1/gfield-hq/main/GFIELD_MEMORY/HF_SVG_TASK_ORDER.md
```

### 2. 전체 아키텍처 설계도
```
https://raw.githubusercontent.com/docssam1/gfield-hq/main/GFIELD_MEMORY/HF_ARCHITECTURE.md
```

### 3. 기존 tutor-scripts.js (54개 유형 데이터)
```
https://raw.githubusercontent.com/docssam1/Hyper-Focus-answer-Key/main/premier-hyper-focus/data/tutor-scripts.js
```

### 4. 유사문제 데이터
```
https://raw.githubusercontent.com/docssam1/Hyper-Focus-answer-Key/main/premier-hyper-focus/data/sq-a.js
https://raw.githubusercontent.com/docssam1/Hyper-Focus-answer-Key/main/premier-hyper-focus/data/sq-b.js
https://raw.githubusercontent.com/docssam1/Hyper-Focus-answer-Key/main/premier-hyper-focus/data/sq-c.js
```

---

## 결과물 1 — hf_runtime.py

기존 `type4_runtime.py`를 아래 규칙에 따라 54개 유형 전체로 확장:

### 변경 규칙
- `TYPE_ID = 4` → 파라미터 `type_id` 로 변경
- 모든 함수명 `build_type4_` → `build_hf_`
- 모든 클래스명 `Type4` → `HF`
- 파일명: `hf_runtime.py`

### lockPolicy 구조 반영
```python
LOCK_POLICY = {
    "lv1": {
        "aiTutorDailyLimit": 2,
        "visionAnalysisLimit": 2,
        "handwritingScope": "fixedSimilarsOnly",
        "audioScope": "fixedSimilars+parentGuide",
        "aiGeneratedSimilarLimit": 1,
        "pdfScope": "selectedOne",
        "adsEnabled": True
    },
    "lv2": {
        "aiTutorDailyLimit": -1,
        "visionAnalysisLimit": 5,
        "handwritingScope": "all",
        "audioScope": "all",
        "aiGeneratedSimilarLimit": -1,
        "pdfScope": "all",
        "adsEnabled": False
    }
}
```

### 오디오 정책
- `conceptAudioPath`: null 허용
- null이면 오디오 버튼 숨김 처리
- `audioScript` 필드 별도 생성

### handwritingData 구조
```python
"handwritingData": {
    "svgPath": "M10 10 C 20 20, 40 20, 50 10",
    "duration": 2000,
    "color": "#FF0000",
    "emphasisTrigger": "CALCULATION_ERROR"
}
```

### 오답 라우팅
- CALCULATION_ERROR → SAME 난이도, YellowClinicCard
- CONCEPT_ERROR → EASY 난이도, RedClinicCard
- NONE (정답) → HARD 난이도, GreenWinCard

### 금지어 필터
```python
BLOCKED_WORDS = ["교차점", "단면화", "단면", "교차"]
```
모든 피드백 텍스트에 금지어 포함 여부 검증 함수 추가.

### 분류 체계
```python
"legacyGroup": "A",           # A(그림39개) 또는 B(텍스트15개)
"functionalGroup": "공간/기하" # 공간/기하, 평면/논리, 연산/규칙, 가중치/활용
```

---

## 결과물 2 — hf_data.json (54개 전체)

### 스키마 (typeId별로 아래 구조)
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
    "renderData": {},
    "audioPath": null
  },
  "fixedSimilars": [
    {
      "questionId": "q01_easy_1",
      "difficulty": "easy",
      "text": "문제 텍스트",
      "answer": "정답",
      "answerStory": "풀이 스토리",
      "handwritingData": {
        "svgPath": "사람이 쓴 듯한 자연스러운 곡선 SVG Path 문자열 (Bezier 곡선 포함)",
        "duration": 2000,
        "color": "#FF0000",
        "emphasisTrigger": "CALCULATION_ERROR"
      },
      "audioPath": null,
      "audioScript": "[도입] → [핵심 개념] → [실수 방지 팁] → [격려] 30초 이내"
    }
  ],
  "aiTutorPack": {
    "conceptAudioPath": null,
    "audioScript": "독쌤 음성 스크립트",
    "problemPool": {
      "easy": [],
      "same": [],
      "hard": []
    }
  },
  "flowController": {
    "routes": {
      "CALCULATION_ERROR": {},
      "CONCEPT_ERROR": {},
      "NONE": {}
    }
  },
  "stitchesUi": {
    "schemaVersion": "hf-v1",
    "cards": {}
  },
  "adPolicy": {
    "lv1BannerEnabled": true,
    "lv1InterstitialTriggers": ["tutorLimitReached", "pdfExport"]
  }
}
```

### 중요 원칙
- tutor-scripts.js의 `scriptSummary`, `docssamExplanation`, `hint`, `parentTip` 반드시 참고
- sq-a/b/c.js의 기존 question 텍스트와 다른 숫자/조건 사용
- 모든 텍스트에서 금지어(교차, 단면 등) 사용 금지
- 유아어 우선: '교차점' → '길이 만나는 곳', '단면' → '잘린 면' 등
- **handwritingData.svgPath: 반드시 사람이 쓴 듯한 자연스러운 Bezier 곡선(C, Q 명령어 포함) SVG Path 문자열로 생성**
- audioScript: [도입] → [핵심 개념 1문장] → [실수 방지 팁] → [격려] 30초 이내

### 출력 형식
- JSON 파일 하나로 54개 전체 배열
- 다른 텍스트 없이 JSON만 출력
- 파일명: `hf_data.json`

---

## 결과물 3 — viewer_handwriting.js (Vivus.js + Khoshnus.js 연동)

### 목적
viewer-ai-tutor.html이 hf_data.json의 handwritingData를 받아서
Vivus.js(도형/격자)와 Khoshnus.js(수식 텍스트)로 손글씨 애니메이션 재생.

### HTML 구조 (viewer에 이미 있어야 할 것)
```html
<!-- Vivus.js CDN -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/vivus/0.4.6/vivus.min.js"></script>

<!-- 손글씨 영역 -->
<svg id="handwriting-svg" viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg">
  <path id="handwriting-path" d="" stroke="#FF0000" stroke-width="2" fill="none"/>
</svg>
```

### 연동 코드 (5줄 핵심)
```javascript
function playHandwriting(handwritingData) {
  // 1. SVG Path 주입
  document.getElementById('handwriting-path').setAttribute('d', handwritingData.svgPath);

  // 2. 색상 적용
  document.getElementById('handwriting-path').setAttribute('stroke', handwritingData.color || '#FF0000');

  // 3. Vivus 실행
  new Vivus('handwriting-svg', {
    duration: handwritingData.duration || 2000,
    type: 'delayed',
    pathTimingFunction: Vivus.EASE
  });
}
```

### 강조 트리거 처리
```javascript
// CALCULATION_ERROR일 때 강조 애니메이션
if (handwritingData.emphasisTrigger === 'CALCULATION_ERROR') {
  document.getElementById('handwriting-path').style.strokeWidth = '4';
  document.getElementById('handwriting-path').style.stroke = '#FF0000';
}
```

### 수식 텍스트용 (Khoshnus.js)
```javascript
// 수식(예: 27-5=22)을 글자별로 손글씨처럼 쓰는 효과
// Khoshnus는 별도 CDN 추가 필요
function playMathHandwriting(formulaText) {
  const instance = new Khoshnus('#math-handwriting-svg', {
    font: 'Parisienne'
  });
  instance.write(formulaText, {
    writeConfiguration: { eachLetterDelay: 200 }
  });
}
```

### 출력 파일명
`viewer_handwriting.js`

---

## [지시서 끝]

완성 후 결과물 3개를 GitHub에 올려줘:
```
repo: docssam1/Hyper-Focus-answer-Key
branch: main
hf_runtime.py        → premier-hyper-focus/data/hf_runtime.py
hf_data.json         → premier-hyper-focus/data/hf_data.json
viewer_handwriting.js → premier-hyper-focus/data/viewer_handwriting.js
```
