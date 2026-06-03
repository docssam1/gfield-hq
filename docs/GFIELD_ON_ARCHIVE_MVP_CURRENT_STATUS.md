# GFIELD-ON Archive MVP Current Status

작성 목적:

이 문서는 GFIELD-ON Archive 1차 MVP의 현재 판단 기준을 기록하기 위한 현재 상태 문서다.
승인 요청서가 아니라 관제 판단과 작업 라인 분리 기준이다.
민감한 운영 데이터나 실제 자료 링크는 포함하지 않는다.

---

## 1. 핵심 판단

GFIELD-ON은 현재 리포트 시스템이 아니다.
GFIELD-ON은 학부모/재원생에게 보낼 수 있는 독립 승인형 프리미엄 자료실 MVP로 본다.

현재 단계에서 GFIELD-ON은 gfield report 3 운영본과 분리한다.
향후 리포트 하단에 GFIELD-ON 링크를 넣는 것은 가능하지만, 지금은 리포트 운영본과 코드, 데이터, 자료 구조를 섞지 않는다.

---

## 2. 1차 MVP 범위

1차 범위는 다음으로 제한한다.

```text
1. 인트로
2. 이름 + 승인번호 입장
3. 황소 대비 자료실
4. 프리미어 자료실
5. eBook viewer 연결
```

1차 목표는 외부 홍보 홈페이지가 아니라 링크를 보내도 되는 자료실 MVP를 안정화하는 것이다.

---

## 3. 보류 범위

다음은 1차에서 보류한다.

```text
- 학생별 DB
- 결제 / 회원가입
- 리포트 연결
- 뉴스 자동화
- 카카오톡 분석
- Report Archive 자동 연결
- 날씨 / 교통 브리핑 자동화
- Video Linker 자동 매칭
- OCR 전체 자동화
```

---

## 4. 작업 라인 분리

### Archive 라인

역할:

```text
화면 / 감성 문구 / 자료실 카드 / 모바일 UI / viewer 연결
```

담당 범위:

```text
- intro
- 이름 기반 입장
- 승인번호 또는 접근 코드
- 아이 이름 / 어머님 감성 문구
- 황소 대비 자료실
- 프리미어 자료실
- library / archive 화면
- eBook / 영상 viewer 연결
- 모바일 감성 UI
- MP4 배경 또는 카드 모션
```

하지 말 것:

```text
- EBOOK SCAN 로직 구현
- PDF/HWP 이미지화 직접 구현
- 학생별 권한 DB 구현
- 리포트 운영본 연결
- 결제/회원가입 구현
```

### EBOOK SCAN 라인

역할:

```text
PDF/HWP 이미지화 / book_id 부여 / 썸네일 / manifest.json 생성
```

담당 범위:

```text
- 원본 자료 입력 기준 정리
- Book ID 부여
- 페이지 이미지 생성
- 썸네일 생성
- manifest.json 생성
- pages 배열 생성
- page_width / page_height 저장
- source_info 저장
- materials.json 연결용 book_id / thumbnail_path / targetUrl 정보 제공
```

하지 말 것:

```text
- Archive UI 수정
- index.html / library.html 임의 수정
- 감성 문구 수정
- 학생별 권한 DB 구현
- 리포트 연결
- 카카오톡 분석
- Video Linker 자동 매칭
```

---

## 5. materials / manifest 기준

세부 JSON 표준과 materials / manifest 필드는 별도 실무 별첨을 참고한다.

현재 관제 기준에서는 다음만 확정한다.

```text
materials.json = Archive / library / viewer가 읽는 자료 카드 목록
manifest.json = eBook viewer가 한 권을 열 때 읽는 상세 페이지 구조
```

---

## 6. 이름 기반 입장 기준

현재 이름 기반 입장은 정식 회원 로그인으로 보지 않는다.
MVP에서는 개인화 표시와 약한 접근 제어까지만 허용한다.

허용:

```text
- 이름 표시
- 어머님 호칭 표시
- 화면 상단 개인화 문구
- 워터마크 표시
- 자료실 입장
- 황소 / 프리미어 자료 구분
- 승인번호 입력 후 접근
```

불허:

```text
- 실제 성적표 원본 노출
- 민감 리포트 자동 노출
- 결제 정보 노출
- 카카오톡 원본 노출
- 이름만으로 민감 자료 접근
```

---

## 7. 디자인 / 감성 기준

현재 디자인은 승인 전 시안이다.
디자인 방향은 정하되, 최종 승인 전 전체 교체로 보지 않는다.

방향:

```text
- 딥그린
- 골드
- 아이보리
- 블랙톤
- 프리미엄 자료실
- 모바일은 감성적으로 화려하게
- 웹은 고급스럽고 안정적으로
```

MP4 사용 기준:

```text
- autoplay
- muted
- loop
- playsinline
- poster 이미지 사용 권장
- 핵심 버튼과 텍스트 가독성을 방해하지 않음
```

모바일 기준:

```text
모바일이라고 단순 세로 리스트만 고집하지 않는다.
가로 와이드 카드, 스와이프 카드, 영상형 배경을 사용할 수 있다.
다만 핵심 진입 버튼은 첫 화면에서 명확해야 한다.
```

---

## 8. hub / 뉴스 / 날씨 / 교통 감성 레이어

hub.html에 있던 감정선 문구, 뉴스 큐레이터, 날씨/교통 브리핑은 GFIELD 브랜드 경험 자산으로 본다.

다만 1차 MVP의 핵심에는 넣지 않는다.

판단:

```text
1차에 넣지 않는다.
자리만 열어둔다.
```

향후 후보:

```text
- archive_hub.html
- dashboard.html
- today_briefing_widget
- news_curator_widget
- traffic_briefing_widget
```

---

## 9. 현재 금지 사항

```text
- gfield report 3 운영본 수정 금지
- 리포트 원본 연결 금지
- 학생별 실제 DB 구현 금지
- 결제 / 회원가입 구현 금지
- 뉴스 큐레이터 자동화 금지
- 카카오톡 분석 연결 금지
- 원본 PDF/HWP/이미지 GitHub 업로드 금지
- 실제 Drive 링크 GitHub 기록 금지
- 비밀값 커밋 금지
```

---

## 10. 관제 결론

```text
GFIELD-ON 1차는 승인형 프리미엄 자료실 MVP이다.
핵심은 Archive UI와 EBOOK SCAN 라인을 분리하는 것이다.
지금은 materials.json과 manifest.json 표준을 참고하되,
학생별 DB·결제·리포트·뉴스 자동화는 보류한다.
```

현재 실행 우선순위:

```text
1. Archive MVP 안정화
2. EBOOK SCAN 라인 기준 분리
3. materials / manifest 표준 참고
4. 디자인은 승인 전 시안으로만 적용 검토
```
