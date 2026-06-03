# GFIELD Control Advisory Role Map

작성 목적:

이 문서는 GFIELD 관제 자문실이 기억해야 할 핵심 역할 분리표입니다.
민감정보, 실제 Drive 공유 링크, API Key, Telegram Bot Token, 서비스계정 JSON, 학생 개인정보 원문은 포함하지 않습니다.

---

## 1. 기본 원칙

- 관제 자문실은 상시 실행 주체가 아니라 구조 판단, 위험 검토, 작업 순서 정리, Codex 작업 지시서 작성, 결과 검수를 담당한다.
- 실제 코드 수정, 파일 수정, GitHub 반영, 서버 작업은 Codex 계열 작업자가 담당한다.
- GFIELD-ON 및 콘텐츠 총괄 GPT는 콘텐츠 구조, 자료실, eBook, 권한/저작권/포털 구조를 판단한다.
- 민감 자료의 존재와 위치는 관리해야 하지만, GitHub에는 원문이나 실제 링크를 기록하지 않는다.
- gfield report 3 운영본은 보호 대상이며, 실험/자동화/Archive와 섞지 않는다.
- 확인되지 않은 내용은 “확인 필요”로 표시하고, 실행 전 실제 파일/문서/로그로 검증한다.

---

## 2. 현재 역할 카드

### 2.1 할아버지 GPT

역할:

- 전임 전체 총괄
- Hermes / GFIELD-ON / 리포트 / 카톡 / Drive / 자료실 전체 지도 제공
- 확실 / 추정 / 확인 필요를 구분한 인수인계 자료 제공

주의:

- 할아버지 GPT의 내용도 최종 확정 자료가 아니다.
- 관제 자문실은 실제 GitHub 문서, VM 로그, 파일 구조와 비교해 검수해야 한다.

---

### 2.2 GFIELD-ON 및 콘텐츠 총괄 GPT

역할:

- 콘텐츠 구조 총괄
- GFIELD-ON / Content OS / 자료실 / eBook / Video Linker / Access Control / 저작권 / Portal 구조 판단
- 수학, 영어, 과학, 코칭, 로드맵, 공지 등 다과목 콘텐츠 플랫폼 설계

가능한 권한:

- Book Registry 구조 제안
- subject / category / type 구조 설계
- eBook과 영상 연결 기준 제안
- 워터마크, 저작권 상태, 접근권한 정책 제안
- GFIELD-ON 1차 MVP 범위 제안

넘으면 안 되는 권한:

- 서버 구조 확정
- 실제 GitHub 반영
- VM 작업 직접 실행
- 학생별 실제 권한 DB 확정
- 자동 공개 / 자동 발송 확정
- 저작권 위험 자료 공개 결정

---

### 2.3 GFIELD-ON Archive 작업자

구분:

- Codex 쪽 실행 작업자

역할:

- GFIELD-ON 포털 화면 작업
- `index.html` 승인번호 게이트
- `library.html` 서재 / 자료실 허브
- `premier_archive.html` eBook / 영상 viewer
- 서재 → viewer → 서재 복귀 흐름 점검
- materials.json fetch, fallback, viewer id 매칭, 모바일 레이아웃 등 포털 안정화

주의:

- gfield report 3 운영본을 건드리지 않는다.
- 학생별 실제 권한 DB, 자동 공개, 자동 발송은 구현하지 않는다.
- 승인번호 게이트는 강한 보안 로그인으로 보지 않는다.

---

### 2.4 EBOOK SCAN 작업자

구분:

- GPT가 아니라 Codex 쪽 실행 작업자

역할:

- 교재/자료 원본을 GFIELD-ON에서 사용할 수 있도록 페이지 이미지화
- Book ID 기준 분류
- 썸네일 생성
- manifest 구조 제안 및 생성 후보
- materials 구조와 연결
- eBook Builder / Portal이 읽을 수 있는 산출물 구조 정리

핵심 정정:

- OCR 작업자가 아니다.
- OCR은 보조 기능일 수 있으나, 1차 역할은 이미지화 / Book ID 분류 / manifest / materials 구조 작업이다.

현재 확인된 상태:

- `THUMBNAIL_PIPELINE.md`는 PDF 첫 페이지 썸네일 생성과 `materials.json`의 `thumbnail_path` 업데이트 범위 문서다.
- 현재 파이프라인은 전체 eBook Factory가 아니다.
- 전체 페이지 이미지화, manifest.json, Book Registry 연동, OCR 파이프라인, 페이지 순서 검수는 별도 기준이 필요하다.

주의:

- 원본 PDF/HWP/HWPX/이미지, OCR 원본, 실제 Drive 링크, 학생명 포함 파일, 유료 자료 원본, `.env`, 토큰/API Key는 GitHub에 올리지 않는다.
- 대량 변환과 OCR은 로컬 PC 메모리 문제를 고려해 worker 서버 후보와 분리 설계가 필요하다.

---

### 2.5 관제 자문실

구분:

- 현재 GPT 자문 채팅

역할:

- 각 GPT/작업자 의견 검수
- 권한 조정
- 충돌 지점 정리
- 작업 우선순위 결정
- Codex 작업 지시서 작성
- 결과 검수
- 위험 변경 차단

주의:

- 직접 상시 실행되는 관제센터가 아니다.
- 실제 구현, 코드 수정, GitHub 반영은 Codex 작업자가 담당한다.

---

## 3. GFIELD-ON 현재 기준

GFIELD-ON은 단순 자료실이 아니라 다과목 콘텐츠 포털이다.

1차 핵심 흐름:

```text
index
→ 승인번호 입력
→ library 서재
→ 자료 카드 선택
→ eBook / 영상 viewer
→ 서재로 복귀
```

현재 확정 가능한 역할 분리:

```text
Google Drive = 원본 저장소
GFIELD-ON Portal = 공개 가능한 열람 화면
GitHub = 코드 / 문서 / 샘플
VM gfield_output = 중간 산출물 / inventory
Sheets 또는 DB = 운영 데이터 / 권한 / 상태값
```

1차에서 제외할 것:

- 완전한 학생 DB
- 결제 기능
- 복잡한 로그인
- 리포트 운영본 자동 반영
- OCR 전체 자동화
- 학생별 고급 권한 시스템
- 모든 과목 자료 대량 등록

---

## 4. 리포트 운영본 보호 원칙

운영본:

```text
G:\내 드라이브\코딩관련\field_report 3
```

프로젝트명:

```text
gfield report 3
```

원칙:

- 현재 실제 운영 중인 리포트 시스템으로 본다.
- 실험용으로 건드리지 않는다.
- 자동인식, Report Archive, GFIELD-ON과 직접 섞지 않는다.
- 자동인식 프로젝트는 초안 생성까지만 담당하고, 운영본 반영은 승인 후 진행한다.

실험본:

```text
G:\내 드라이브\코딩관련\gfield_report IV
```

원칙:

- 차기 개발/실험본이다.
- 운영본이나 GitHub 운영 흐름에 바로 반영하지 않는다.

---

## 5. 서버 확정성 기준

### gfield-hq-vm

상태:

- 현재 관제센터 본부 VM으로 본다.
- gfield-hq 저장소와 연결된 핵심 축이다.
- Telegram Bot, `/run` 명령, Drive scan, Kakao/report inventory 흐름 기준이다.

### gfield-core-vm

상태:

- worker / heavy processing 후보 서버 축이다.
- OCR, 이미지 처리, 대량 변환, API/SMS, 장시간 배치 후보로 본다.
- hq-vm만큼 실체가 확정된 축은 아니므로 확인 필요로 표시한다.

### 기타 VPS / Cloud Run / 고정 IP

상태:

- 과거 논의 또는 일부 흔적이 섞여 있을 수 있다.
- 현재 실운영 여부는 별도 확인 필요다.

---

## 6. GitHub 기록 가능 / 금지 기준

GitHub에 기록 가능:

- 역할표
- 구조 문서
- 작업 지시서
- schema / sample JSON
- 비식별 샘플
- 공개 가능한 README
- 민감정보 없는 테스트 데이터

GitHub에 기록 금지:

- 학생 이름 / 학부모 연락처 / 학교명
- 카카오 원문
- 실제 리포트 원문
- 실제 Drive 공유 링크
- 원본 교재 PDF/HWP/HWPX/이미지
- OCR 원본
- API Key / Token / 서비스계정 JSON / `.env`
- 결제/수납 민감정보

민감 자료 위치 지도는 GitHub가 아니라 서버 비공개 폴더에 둔다.

권장 위치:

```text
/home/gfield7265/gfield_private/
```

---

## 7. 다음 관리 방식

새 역할이 추가될 때는 아래 형식으로 기록한다.

```text
이름:
GPT인지 Codex인지:
맡은 일:
관련 저장소/폴더:
건드리면 안 되는 것:
확실성: 확실 / 추정 / 확인 필요
```

관제 자문실은 이 문서를 기준으로 역할 충돌과 권한 초과를 검수한다.
