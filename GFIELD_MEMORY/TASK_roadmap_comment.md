# 작업 지시서 — 로드맵 코멘트 로직 수정

**작업 ID:** PATCH_roadmap_comment
**작성:** 2026-06-25 (검증 세션)
**처리 주체:** VM 워커 / GPT
**연계 PATCH:** `GFIELD_MEMORY/PATCH_roadmap_comment.md`

---

## 1. PATCH 문서 읽기
- repo: `docssam1/gfield-hq`
- 경로: `GFIELD_MEMORY/PATCH_roadmap_comment.md`
- raw: `https://raw.githubusercontent.com/docssam1/gfield-hq/main/GFIELD_MEMORY/PATCH_roadmap_comment.md`

## 2. 수정 대상 (둘 다 — 같은 수정 3쌍 적용)
- repo: `docssam1/lete-on` (branch: main)
  - ① `roadmap/index.html`
  - ② `roadmap/demo/index.html`

## 3. 적용 방법
- PATCH 문서의 "수정 1·2·3" 각 항목의 **[찾기] 블록을 [바꾸기] 블록으로 그대로 교체**.
- 찾기 문자열은 각 파일에 **정확히 1회만** 존재 → 그 1곳만 교체.
- **두 파일 모두 동일하게 3곳씩 교체 (총 6곳).**
- 그 외 코드·문구는 **절대 건드리지 말 것.**

## 4. 적용 전 확인
- 각 파일에서 [찾기] 문자열이 정확히 1회 매칭되는지 grep으로 먼저 확인.
- 0회 또는 2회 이상이면 **중단하고 보고** (이미 적용됐거나 원본 변경됨).

## 5. 적용 후 검증
- `node --check`로 JS 문법 오류 없는지 확인 (각 파일 script 추출).
- 각 파일에 `calcBehindSchool` 3회 / `thinkingOnlyBehind` 3회 들어갔는지.
- `연산을 교과 수준에 맞춰 다시 설정` 1회 들어갔는지.

## 6. 커밋 & 배포
- commit msg:
  `fix(roadmap): 코멘트 로직 — 연산<교과 재설정 경고 + 사고력만 뒤처짐=좋은신호 (PATCH_roadmap_comment 적용)`
- push → main → GitHub Pages 반영 확인
- 배포: 텔레봇 `/run`

## 7. 완료 보고
- 두 파일 커밋 SHA
- 검증 결과 (문법 OK, 매칭 6곳 교체 완료)
- 화면 확인 결과 (선택)

---

## 배경 (왜 이 수정인가)
기존 코멘트는 세 축 단순 격차(최대-최소)만 보고 "사고력 N개월 뒤처져 확인 필요"라고만 출력 →
① 연산이 교과보다 뒤처진 순서 위반(잘못된 배치)을 못 잡고,
② 교과는 됐는데 사고력만 뒤처진 "좋은 신호"를 "멈추라"고 잘못 안내.
이를 (연산 ≥ 교과 ≥ 사고력) 순서 진단으로 교정.

**작성 측 사전 검증 완료:** JS 문법 OK(두 파일 node --check), 분기 6종 시뮬레이션 정확 동작.
