# HF 작업 지시서 01 — hf_runtime.py 작성

> Gemini 2.5 Pro AI Studio에 아래 내용을 그대로 붙여넣을 것

---

## [지시서 시작]

너는 GFIELD 프리미어 하이퍼 포커스 AI 튜터 시스템의 백엔드 개발자야.
기존 `type4_runtime.py`를 54개 유형 전체로 확장한 `hf_runtime.py`를 작성해줘.

---

## STEP 1. 아래 파일 읽기

### 기존 런타임 (기준)
```
https://raw.githubusercontent.com/docssam1/gfield-hq/main/GFIELD_MEMORY/HF_SVG_TASK_ORDER.md
```

### 전체 아키텍처 설계도
```
https://raw.githubusercontent.com/docssam1/gfield-hq/main/GFIELD_MEMORY/HF_ARCHITECTURE.md
```

---

## STEP 2. 변경 규칙

- `TYPE_ID = 4` → 파라미터 `type_id`로 변경
- 모든 함수명 `build_type4_` → `build_hf_`
- 모든 클래스명 `Type4` → `HF`
- 파일명: `hf_runtime.py`

---

## STEP 3. 추가할 것

### lockPolicy
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
"legacyGroup": "A"           # A(그림 39개) 또는 B(텍스트 15개)
"functionalGroup": "공간/기하" # 공간/기하, 평면/논리, 연산/규칙, 가중치/활용
```

---

## 출력 규칙
- Python 파일만 출력 (다른 텍스트 없이)
- 파일명: `hf_runtime.py`

## [지시서 끝]

완성 후 GitHub에 올려줘:
```
repo: docssam1/Hyper-Focus-answer-Key
branch: main
경로: premier-hyper-focus/data/hf_runtime.py
```
