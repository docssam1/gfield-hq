# SIMILAR_HANDOFF_QA 답변 확정본

작성일: 2026-06-18

---

## 1. 역할 분담
- Claude → 설계/PATCH 작성
- GPT → GitHub 파일 fetch/PATCH 적용/push
- Codex → VM 실행
동일하게 유지.

## 2. 회원 등급별 접근 제한
- 현재 미구현
- 추후 설계 필요
- 등급 정보: URL 파라미터 또는 로컬스토리지 방식

## 3. 공개/비공개
- 현재 미구현
- hf_data.json에 "isPublic": true/false 필드 추가 방식으로 구현 예정

## 4. 유사문제 생성 방식
- fixedSimilars 고정 데이터 우선
- AI 자동생성은 AI 튜터 탑재 후 2단계
- 별도 DB 없이 세션 임시 방식

## 5. 이미지 파이프라인
- 01.png~54.png 업로드 미완료 (hf_upload_problems.py 미실행)
- easy/hard 유사문제: 텍스트만 (별도 이미지 없음)
- same(같은 난이도): 원본 이미지 재사용

## 6. 화면 구성
- typeId별 카드 각각 표시
- 카드 구성: 원본 이미지 + 유사문제 텍스트 + 정답/풀이 접기
- 난이도 버튼: 🟢쉬운 / 🟡같은난이도(원본이미지) / 🔴어려운

## 7. 디자인
- 딥블랙(#0f141a) + 브라스골드(#e9c176) Stitch 시스템
- 모바일 우선

## 8. AI 튜터
- Claude API 직접 호출 우선
- 이후 Cloud Run 경유 전환

## 9. 데이터 출처 및 VM 배포
- 소스 txt 4개(ai_studio_code*.txt)가 최종 확정본
- 수정 시: hf_data.json 직접 수정이 가장 효율적
- VM 배포: VM에서 직접 생성 후 git push가 가장 안정적 (이번 세션에서 증명)

---

## 다음 작업 우선순위

1. hf_upload_problems.py 실행 → 01.png~54.png GitHub 업로드
2. 유사문제 카드 UI — Stitch 디자인 적용 (원본이미지 + 텍스트 + 접기)
3. same 선택 시 원본 이미지 렌더링
4. 회원등급 제한 설계 (URL파라미터 기반)
5. AI 튜터 Claude API 직접 호출 연동
