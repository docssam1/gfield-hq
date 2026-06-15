# GFIELD 프리미어 하이퍼 포커스 — 전체 아키텍처 설계도

> 작성: Claude (관호 지시하에) / 2026.06.16  
> 상태: 확정

---

## 1. 파일 구조

```
GFIELD_MEMORY/
  __init__.py           → HF_ 함수 export
  hf_runtime.py         → 핵심 로직 (채점, 피드백, 락 정책)
  hf_data_builder.py    → JSON 데이터 빌드 (54개 유형)

cloud_run_tutor.py      → 채점 엔트리포인트
hf_similar_auto.py      → JSON 생성 엔트리포인트
stitches_router.js      → UI 라우팅 (채점결과 → 카드/모달)
```

---

## 2. Naming Convention

- 파일명: `hf_runtime.py`, `hf_data_{typeId:02d}.json`
- 함수명: `HF_` 접두어 통일
- 클래스명: `HFRuntime`, `HFDataBuilder`
- 기존 `type4_` → 전부 `hf_` 로 교체

---

## 3. 분류 체계 (Taxonomy)

이중 분류 적용:

```json
{
  "legacyGroup": "A",
  "functionalGroup": "공간/기하"
}
```

| legacyGroup | 내용 | typeId |
|---|---|---|
| A | 그림 위주 (SVG/이미지 필요) | 39개 |
| B | 텍스트 위주 | 15개 |

| functionalGroup | 내용 |
|---|---|
| 공간/기하 | 쌓기나무, 전개도, 주사위 |
| 평면/논리 | 색종이, 도형, 논리추리 |
| 연산/규칙 | 수 배열, 규칙, 연산 |
| 가중치/활용 | 공동작업, 비율, 피보나치 |

---

## 4. 2레벨 정책 (lockPolicy)

```json
"lockPolicy": {
  "lv1": {
    "label": "재원생 / 일반판매",
    "aiTutorDailyLimit": 2,
    "visionAnalysisLimit": 2,
    "handwritingScope": "fixedSimilarsOnly",
    "audioScope": "fixedSimilars+parentGuide",
    "aiGeneratedSimilarLimit": 1,
    "pdfScope": "selectedOne",
    "adsEnabled": true
  },
  "lv2": {
    "label": "프리미엄",
    "aiTutorDailyLimit": -1,
    "visionAnalysisLimit": 5,
    "handwritingScope": "all",
    "audioScope": "all",
    "aiGeneratedSimilarLimit": -1,
    "pdfScope": "all",
    "adsEnabled": false
  }
}
```

| 기능 | LV1 (재원생/일반판매) | LV2 (프리미엄) |
|---|---|---|
| 원본 문제 54개 | ✅ | ✅ |
| 유사문제 2개 (fixedSimilars) | ✅ | ✅ |
| 유사문제 AI 튜터 | 하루 2회 체험 | 무제한 |
| 난이도 선택 | ✅ 2회 안에서 | ✅ 무제한 |
| 풀이 분석 (비전) | 2회 체험 | 하루 5회 |
| 손글씨 애니메이션 | 유사문제 2개만 | 무제한 |
| 독쌤 AI 음성 | 유사문제 2개 + 학부모 가이드 | 무제한 |
| AI 생성 유사문제 | 전체 중 1회 체험 | 하루 무제한 |
| PDF 출력 | 선택한 유사문제 1개 | 전체 묶음 |
| 광고 | 있음 | 없음 |

---

## 5. 오디오 정책

```json
"audioPolicy": {
  "conceptAudioPath": null,
  "audioScript": "",
  "fallback": "silent"
}
```

- `conceptAudioPath`: null 허용 — 없으면 오디오 버튼 숨김
- `audioScript`: Gemini TTS 생성용 스크립트 별도 필드
- 스크립트 구조: [도입] → [핵심 개념 1문장] → [실수 방지 팁] → [격려] 30초 이내
- 금지어: 교차, 단면화, 단면, 교차점

---

## 6. 손글씨 애니메이션

**라이브러리:**
- Vivus.js — SVG Path 드로잉 (도형/격자)
- Khoshnus.js — 텍스트 손글씨 (수식)

**데이터 구조:**
```json
"handwritingData": {
  "svgPath": "M10 10 C 20 20, 40 20, 50 10",
  "duration": 2000,
  "color": "#FF0000",
  "emphasisTrigger": "CALCULATION_ERROR"
}
```

**viewer 연동 (5줄):**
```javascript
const pathData = data.handwritingData.svgPath;
new Vivus('handwriting-svg', {
  duration: data.handwritingData.duration,
  type: 'delayed',
  pathTimingFunction: Vivus.EASE
});
```

---

## 7. 오답 라우팅 (flowController)

| 오류 유형 | 난이도 | 카드 | 오디오 |
|---|---|---|---|
| CALCULATION_ERROR | SAME | YellowClinicCard | retryAudio |
| CONCEPT_ERROR | EASY | RedClinicCard | conceptAudio |
| NONE (정답) | HARD | GreenWinCard | 없음 |

**칭찬 샌드위치 원칙:**
- CALCULATION_ERROR: "식은 맞아! 숫자만 다시 콕콕 세어봐"
- CONCEPT_ERROR: "괜찮아! 독쌤 목소리 들으며 다시 찾아보자"

---

## 8. Stitch 디자인 viewer 구조

**디자인 토큰:**
- 배경: `#0f141a` (딥블랙)
- 포인트: `#e9c176` (브라스골드)
- 폰트: Playfair Display (제목), Noto Sans KR (본문)

**레이아웃:**
```
데스크탑:
  헤더 (얇게)
  ↓
  문제 내용 + 영상 (상단)
  ↓
  💬 AI 대화창 (화면 하단 중앙 — ChatGPT 스타일)
    대화 안에서 영상/힌트/풀이/손글씨 모두 처리
  [입력창___________][▶]

모바일:
  흰 배경
  번호 입력 또는 탭 선택
  AI 대화창이 전체 화면
```

**stitches_router.js 카드:**
- YellowClinicCard: accent `sun`, 재시도 버튼
- RedClinicCard: accent `tomato`, 오디오 버튼
- GreenWinCard: accent `mint`, 다음 문제 버튼

---

## 9. 소개 페이지 추가 예정

- AI 튜터 기능 소개 섹션
- LV1 / LV2 기능 비교표
- 광고 영역 (LV1 대상)

---

## 10. 핵심 파일 URL

| 파일 | URL |
|---|---|
| tutor-scripts.js | https://raw.githubusercontent.com/docssam1/Hyper-Focus-answer-Key/main/premier-hyper-focus/data/tutor-scripts.js |
| sq-a.js | https://raw.githubusercontent.com/docssam1/Hyper-Focus-answer-Key/main/premier-hyper-focus/data/sq-a.js |
| sq-b.js | https://raw.githubusercontent.com/docssam1/Hyper-Focus-answer-Key/main/premier-hyper-focus/data/sq-b.js |
| sq-c.js | https://raw.githubusercontent.com/docssam1/Hyper-Focus-answer-Key/main/premier-hyper-focus/data/sq-c.js |
| 원본 이미지 | Drive 폴더 ID: 1jMg0m9l7BTSkjgeAo0OJDVH02fi5qpnn |
| type4_runtime.py (기존) | 업로드 파일 참고 |
