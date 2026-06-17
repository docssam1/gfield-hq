# GFIELD HF 유사문제 시스템 — 작업자 인수 확인 질문지

작성일: 2026-06-18
작성: Claude (대화 기록 전체 검색 기반)

---

## 1. 역할 분담 확인

현재 파악된 워크플로우:
- Claude → 설계/PATCH 작성
- GPT → GitHub 파일 fetch/PATCH 적용/push
- Codex → VM 실행

이 구조가 지금도 동일한가요? 유사문제 작업에서 각자 담당 범위를 확인해 주세요.

---

## 2. 유사문제 데이터 현황 (중요)

이전 세션에서 원장님이 직접 검수하신 sq-a.js / sq-b.js / sq-c.js 3개 파일이 존재했으나 현재 Hyper-Focus-answer-Key repo에서 소멸된 상태입니다.

현재 hf_data.json의 fixedSimilars가 그 변환본이며, 유일한 보존본입니다.

확인 필요:
- sq-a/b/c.js 원본이 Drive나 다른 곳에 백업되어 있나요?
- hf_data.json fixedSimilars가 sq 데이터의 완전한 변환본이 맞나요? 누락된 내용이 있나요?
- sq-c.js에 오타 수정 필요 항목이 있었는데 (달팡이→달팽이 등) hf_data.json에 반영됐나요?
- typeId 23, 24, 28번의 기준 매핑 불일치 문제는 어떻게 처리했나요?

---

## 3. 회원 등급별 접근 제한 (이전 확정 내용 재확인)

이전 세션에서 2티어로 확정:

FREE (무료):
- 원본 문제 1개
- fixedSimilars 2개 (easy 1 + hard 1)
- 힌트
- AI 튜터 하루 N회 제한
- 영상

HYPER PASS (유료):
- 위 전체 무제한
- AI 생성 추가 유사문제
- 손글씨 애니메이션 (Vivus.js + Khoshnus.js)
- 독쌤 AI 음성
- 비전 분석
- PDF 출력

미확정 항목:
- AI 튜터 무료 제한: 하루 N회 vs 문제당 N회? N은 몇 회?
- fixedSimilars 2개 무료 제공 시 easy 1 + hard 1인지, easy 2인지?
- 등급 정보는 어디서 가져오나요? (로컬스토리지, URL파라미터, 서버인증 등)
- 제한 초과 시 처리 방식? (잠금, 광고 후 해제, 업그레이드 유도 등)

---

## 4. 공개/비공개 설정

- 문제별 공개 여부가 다른가요?
- 비공개 문제는 어떻게 표시하나요? (블러, 잠금 아이콘, 완전 숨김)
- 공개/비공개 정보는 hf_data.json 필드로 관리하나요?

---

## 5. 유사문제 화면 구성

- 오답 typeId별 카드가 각각 나오는 구조가 맞나요?
- 카드 안 구성 요소: 원본 문제 이미지 + 유사문제 텍스트인가요?
- same(같은 난이도) 선택 시 원본 이미지를 보여주는 건가요?
- 정답/풀이는 접기(<details>) 방식인가요?
- 난이도 버튼: 쉬운 / 같은난이도 / 어려운 구성이 맞나요?

---

## 6. 유사문제 이미지 파이프라인

현재 상태:
- 원본 54개 문제 이미지: assets/problems/ 에 "{번호} {제목}.png" 형식으로 있음
- hf_upload_problems.py: Drive → GitHub "01.png~54.png" 형식으로 업로드하는 스크립트 있음 (미실행)
- assets/similar/ 폴더: 없음 (SVG 작업 미진행)

확인 필요:
- hf_upload_problems.py 실행해서 01.png~54.png 형식으로 올릴 예정인가요?
- easy/hard 유사문제 이미지는 별도로 만들 예정인가요, 텍스트만 사용하나요?
- 이미지가 아닌 SVG 코드로 저장하는 방향은 유효한가요? (이전 세션에서 합의됨)
- SVG 생성은 Gemini Vision으로 Drive 원본 이미지 참고해서 만드는 방식인가요?
- Drive 원본 이미지 폴더 ID: 1jMg0m9l7BTSkjgeAo0OJDVH02fi5qpnn — 현재도 유효한가요?

---

## 7. 유사문제 생성 방식

이전 세션 확정:
- 방식 1 (우선): sq 데이터 기반 사전 제작 (fixedSimilars)
- 방식 2 (병행): Claude API 실시간 생성

확인 필요:
- hf_similar_auto.py (Hyper-Focus-answer-Key repo에 있음)가 실시간 생성 역할인가요?
- AI 생성 유사문제는 어디에 저장하나요? (hf_data.json 업데이트, 세션 임시, 별도 DB)

---

## 8. 유사문제 데이터 수정/추가 방법

이전에 원장님이 한 문제 한 문제 직접 검수하신 데이터입니다.
추후 수정/추가 시 가장 효율적인 방식이 무엇인지 확인이 필요합니다:

A. hf_data.json 직접 수정
B. sq-a/b/c.js 원본 복원 후 재변환
C. Google Sheets 등 별도 관리 도구
D. AI Studio에서 재생성

그리고 대용량 JSON을 GitHub에 안정적으로 올리는 방법:
현재 GitHub API 청크 방식은 불안정했음. VM에서 직접 생성 후 git push가 가장 안정적임.

---

## 9. AI 튜터 연동

- 유사문제 풀이 후 Claude API 힌트/해설 기능 계획 있나요?
- Cloud Run 서버 경유인가요, 클라이언트 직접 호출인가요?
- tutor-scripts.js (소멸됨) 복원 계획이 있나요?

---

## 10. 디자인

- 딥블랙(#0f141a) + 브라스골드(#e9c176) Stitch 시스템 적용인가요?
- 모바일 우선인가요?
- 현재 임시로 들어간 기본 스타일(.sim-diff-btn 등)은 전면 교체 예정인가요?
