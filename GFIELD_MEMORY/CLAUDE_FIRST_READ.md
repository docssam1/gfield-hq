# CLAUDE_FIRST_READ
> 새 채팅창 열 때 반드시 이 파일을 먼저 읽고 아래 템플릿을 첫 메시지에 붙여넣을 것

---

## 복붙용 세션 시작 템플릿

```
이 프로젝트는 GFIELD 작업입니다.

먼저 아래 공통 원칙 문서를 기준으로 작업하세요.

1. WORKER_OPERATING_RULES
https://github.com/docssam1/gfield-hq/blob/main/GFIELD_MEMORY/WORKER_OPERATING_RULES.md

2. 현재 작업 컨텍스트
https://github.com/docssam1/gfield-hq/blob/main/GFIELD_MEMORY/HF_SVG_TASK_ORDER.md
https://github.com/docssam1/gfield-hq/blob/main/GFIELD_MEMORY/HF_SVG_PATCH_WORKFLOW.md
https://github.com/docssam1/gfield-hq/blob/main/GFIELD_MEMORY/HF_SIMILAR_AUTO_SCRIPT.md

공통 작업 원칙:
- 작업 전 계획/의견 먼저 보고 → 원장님 승인 후 실행
- 승인 전 파일 수정·업로드·커밋·푸시 금지
- 줄 번호로 지시하지 마라
- 파일명, 찾을 기존 블록, 교체할 새 블록만 작성
- 직접 수정하지 말고 PATCH_REQUEST만 작성
- 전체 파일 새로 쓰기 금지
- 토큰 낭비 금지 — 필요한 조각만 읽을 것
- 모르면 추측하지 말고 "확인 필요" 보고 후 멈출 것
```

---

## 현재 프로젝트 상태 (2026.06.15 기준)

### 완료된 것
- tutor-scripts.js — hint1/hint2→hint, videoUrl 54개 완성
- viewer-ai-tutor.html — AI 튜터 뷰어 (슬라이드 영상, 연습 1/2 탭)
- sq-a/b/c.js — 유사문제 데이터 54개 완성
- PATCH 워크플로우 확정
- 유사문제 이미지 분류표 확정 (A:그림 39개 / B:텍스트 15개)
- 자동화 스크립트 작성 (HF_SIMILAR_AUTO_SCRIPT.md)

### 다음 작업
1. Cloud Shell에서 HF_SIMILAR_AUTO_SCRIPT.md 실행
   → Drive 이미지 → GitHub assets/similar/ 업로드
   → sq-a/b/c.js imgUrl 자동 패치
2. viewer-ai-tutor.html 전면 재설계
   → Stitch 디자인 (딥블랙+골드)
   → AI 대화창 화면 하단 중앙 (ChatGPT 스타일)
   → 모바일: 흰 배경, 번호 선택
3. 유사문제 PDF 출력 기능

### 핵심 파일 위치
| 파일 | 위치 |
|------|------|
| tutor-scripts.js | Hyper-Focus-answer-Key/premier-hyper-focus/data/ |
| sq-a/b/c.js | Hyper-Focus-answer-Key/premier-hyper-focus/data/ |
| viewer-ai-tutor.html | Hyper-Focus-answer-Key/premier-hyper-focus/ |
| 원본 이미지 | Drive 폴더 ID: 1jMg0m9l7BTSkjgeAo0OJDVH02fi5qpnn |
| GFIELD_MEMORY | docssam1/gfield-hq/GFIELD_MEMORY/ |
| 자동화 스크립트 | GFIELD_MEMORY/HF_SIMILAR_AUTO_SCRIPT.md |
| PATCH 워크플로우 | GFIELD_MEMORY/HF_SVG_PATCH_WORKFLOW.md |
