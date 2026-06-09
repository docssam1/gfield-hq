# GFIELD-ON Archiv 파일럿 Drive + Manifest 최종 락

> 이 문서는 GFIELD-ON Archiv 파일럿의 원천 자산 저장, manifest, viewer-v2 로딩, 인쇄/워터마크, 향후 bbox 오답노트 확장을 위한 최종 합의 기준이다.  
> 기준일: 2026-06-09  
> 상태: Final Lock / 파일럿 기준

---

## 0. 최종 결론

GFIELD-ON Archiv 파일럿은 유료 GCS를 1차 원본 저장소로 쓰지 않는다.

원장님 Google Drive를 원본 자산 저장소로 사용한다.

단, viewer는 `webContentLink`를 직접 저장하거나 고정 이미지 URL로 사용하지 않는다.

각 교재는 `bookId` 단위로 관리하고, 각 페이지는 `manifest.json` 안의 `driveFileId`, `fileName`, `width`, `height`, `mimeType`으로 관리한다.

1차 파일럿에서는 Drive `fileId` 기반 표시 링크를 임시 사용할 수 있다.  
운영 안정화 단계에서는 인증/권한/트래픽 관리를 위해 Cloud Run / Apps Script / VM 중 하나의 경량 프록시 구조로 전환한다.

---

## 1. 역할 분담 최종 락

### UI 구조

관제센터안 채택.

- 9대 대분류 콤팩트 탭
- 서재 UX
- 책 카드 / 책 선택 / 상세 설명
- 강의 연결형 viewer 진입

### 백엔드 적재·로딩 구조

파일럿 팀안 채택.

- Google Drive 원본 저장
- `fileId + manifest.json` 기반 관리
- `webContentLink` 고정 저장 금지
- 최종 운영은 인증/프록시 구조 전환 가능하게 설계

### 최종 조합

```text
UI = 관제센터안
자산 저장/로딩 = 파일럿 팀안
최종 원칙 = Google Drive 원본 저장 + manifest 기반 + viewer-v2 렌더링
```

---

## 2. Google Drive 원천 자산 폴더 규격

한글 공백 및 특수문자로 인한 파이썬 업로드 오류를 줄이기 위해 Drive 내부 저장명은 영문 소문자, 숫자, 하이픈, 언더바 중심으로 관리한다.

기본 구조:

```text
Google Drive
└─ 01_Math_Archive
   └─ didimdol_thinking
      └─ didimdol-thinking-001
         ├─ cover.jpg
         ├─ manifest.json
         └─ pages
            ├─ page-001.jpg
            ├─ page-002.jpg
            └─ page-003.jpg
```

### 파일명 규칙

페이지 파일명은 아래 형식으로 확정한다.

```text
page-001.jpg
page-002.jpg
page-003.jpg
```

3자리 번호를 기본으로 사용한다.  
대부분 교재는 999쪽을 넘지 않으므로 3자리로 충분하다.

---

## 3. 9대 대분류 폴더 원칙

파일럿/확장 설계에서는 9대 대분류를 둘 수 있다.

예시:

```text
01_Math_Archive
02_English_Archive
03_Science_Archive
04_Coaching_Archive
05_Roadmap_Archive
06_Report_Archive
07_Notice_Archive
08_Video_Archive
09_Admin_Archive
```

현재 파일럿 우선순위는 `01_Math_Archive`이다.

---

## 4. category_id / subcategory_id 규칙

폴더명과 데이터 식별자는 분리하되, 되도록 대응 가능하게 둔다.

예시:

```json
{
  "category_id": "math_archive",
  "subcategory_id": "didimdol_thinking"
}
```

사용 예:

```text
01_Math_Archive / didimdol_thinking / didimdol-thinking-001
```

---

## 5. bookId 규칙

교재 단위는 `bookId`로 고정한다.

형식:

```text
publisher-series-level-volume
```

예시:

```text
didimdol-thinking-001
didimdol-elementary-2a
didimdol-calculation-2a
hs-thinking-basic
```

원칙:

- 영문 소문자
- 공백 금지
- 한글 금지
- 특수문자 최소화
- 하이픈 사용
- 한번 정하면 변경 금지

---

## 6. manifest.json 기본 스펙

기본형:

```json
{
  "content_id": "ebook_didimdol_thinking_001",
  "bookId": "didimdol-thinking-001",
  "title": "디딤돌 사고력 수학 1-1",
  "category_id": "math_archive",
  "subcategory_id": "didimdol_thinking",
  "content_type": "ebook",
  "purchaseUrl": "",
  "cover": {
    "fileName": "cover.jpg",
    "driveFileId": "DRIVE_THUMB_FILE_ID_000"
  },
  "pages": [
    {
      "pageNo": 1,
      "fileName": "page-001.jpg",
      "driveFileId": "DRIVE_PAGE_FILE_ID_111",
      "mimeType": "image/jpeg",
      "width": 1240,
      "height": 1754
    }
  ]
}
```

---

## 7. 나중에 추가할 manifest 필드

지금 당장은 필수로 넣지 않는다.  
다만 향후 확장을 위해 아래 필드를 열어둔다.

```text
pageLabel
isPreview
watermarkRequired
linkedVideos
linkedWorksheets
bboxMap
```

확장 예:

```json
{
  "pageNo": 35,
  "fileName": "page-035.jpg",
  "driveFileId": "DRIVE_PAGE_FILE_ID_035",
  "mimeType": "image/jpeg",
  "width": 1240,
  "height": 1754,
  "pageLabel": "35",
  "isPreview": false,
  "watermarkRequired": true,
  "linkedVideos": [],
  "linkedWorksheets": [],
  "bboxMap": []
}
```

---

## 8. Drive 이미지 로딩 기준

### 금지

```text
webContentLink를 DB나 HTML에 영구 이미지 주소처럼 저장하지 않는다.
```

`webContentLink`는 다운로드 링크 성격이 강하고, 안정적인 이미지 CDN 주소로 쓰는 구조가 아니다.

### 1차 파일럿 허용

1차 파일럿에서는 Drive `fileId` 기반 표시 URL을 임시로 사용할 수 있다.

예:

```javascript
function getSafeViewerImageUrl(driveFileId) {
  if (!driveFileId) return 'assets/placeholder.jpg';
  return `https://docs.google.com/uc?export=view&id=${driveFileId}`;
}
```

단, 위 방식은 최종 운영용 안정 프록시가 아니다.

### 최종 운영 기준

운영 안정화 단계에서는 아래 중 하나로 전환한다.

```text
Cloud Run 경량 프록시
Apps Script 경량 프록시
VM 경량 프록시
```

최종 목표:

```text
manifest → driveFileId → 인증/프록시 표시 URL → viewer-v2 렌더링
```

---

## 9. viewer-v2 렌더링 기준

viewer-v2는 manifest를 읽어 페이지를 표시한다.

기본 흐름:

```text
bookId 확인
→ manifest.json 로드
→ pages 배열 확인
→ 현재 pageNo의 driveFileId 확인
→ 표시 URL 생성
→ viewerPageImage에 표시
```

기본 함수 형태:

```javascript
function renderPageFromManifest(pageData) {
  const imgElement = document.getElementById('viewerPageImage');
  imgElement.src = getSafeViewerImageUrl(pageData.driveFileId);
  imgElement.style.width = `${pageData.width}px`;
  imgElement.style.height = `${pageData.height}px`;
}
```

주의:

- 이 코드는 구조 예시다.
- 실제 운영에서는 화면 크기에 맞춰 `object-fit: contain` 또는 CSS scale 방식으로 표시한다.
- 모바일에서는 세로 스택이 아니라 화면 안에 전체 페이지가 들어오도록 축소해야 한다.

---

## 10. 모바일 viewer-v2 기준

강의가 나오는 viewer-v2는 다음 구조가 기준이다.

```text
왼쪽: 강의 영상
오른쪽: 강의 교재 화면
```

모바일에서도 원칙은 유지한다.

금지:

```text
모바일 세로에서 영상 위 / 교재 아래로 세로 스택 전환
교재가 잘려서 세로 스크롤로만 보이는 구조
아래 가로 스크롤
```

원칙:

```text
강의 + 교재 동시 보기
교재 이미지는 전체 화면 안에 맞게 축소
한 페이지 전체보기 우선
책만 보기에서는 교재 100% 확장
영상만 보기에서는 영상 100% 확장
```

---

## 11. 외부 교재 표시 기준

외부 교재는 다음 구조로 표현한다.

```text
외부 교재 eBook 무료 제공 ❌
구매한 교재로 듣는 지필드 강의 ⭕
```

서재 상세 버튼:

```text
교재 구매하기
구매한 교재로 강의 보기
```

강의 뷰어:

```text
왼쪽: 지필드 강의 영상
오른쪽: 강의 교재 화면
```

교재 화면은 보여줄 수 있다.  
단, 표현은 “구매한 교재와 함께 보는 강의 화면”으로 잡는다.

---

## 12. 인쇄/워터마크 기준

인쇄는 가능하다.

단, 워터마크는 필수다.

```text
인쇄 가능 ⭕
다운로드 자유 제공 ❌
워터마크 없는 인쇄 ❌
```

화면 보기:

```text
은은한 워터마크
```

인쇄:

```text
선명한 워터마크
대각선 반복 워터마크
학생명 포함
출력일 포함
지필드 영재교육 포함
승인 학생 전용 문구 포함
```

권장 문구:

```text
GFIELD-ON Archiv
지필드 영재교육
승인 학생 전용
학생명: ○○○
출력일: YYYY-MM-DD
```

또는:

```text
지필드 영재교육 승인 학생 전용 자료
무단 공유 및 재배포 금지
학생명: ○○○
```

---

## 13. 문항 bbox 좌표 매핑 원칙

문항 이미지를 미리 대량 절단하지 않는다.

기본 원칙:

```text
저장은 통 페이지 이미지
사용은 좌표로 쪼개기
```

예시:

```json
{
  "bookId": "didimdol-thinking-001",
  "page": 35,
  "problemId": "p035_q04",
  "label": "4번",
  "bbox": {
    "x": 0.08,
    "y": 0.42,
    "w": 0.84,
    "h": 0.16
  }
}
```

좌표는 가능하면 픽셀이 아니라 0~1 비율 좌표로 저장한다.

이유:

```text
PC / 태블릿 / 모바일 / 확대 / 축소 환경에서 위치 유지
```

---

## 14. 오답노트 확장 시나리오

학생이 “독해력 1단계 35쪽 4번”을 틀렸다고 입력한다.

처리 순서:

```text
bookId 확인
→ page-035.jpg 확인
→ p035_q04 좌표 확인
→ 해당 영역을 canvas 또는 서버 crop으로 표시
→ 오답노트 PDF 또는 화면에 삽입
```

파일럿 단계에서는 crop 자동화를 무리하게 먼저 구현하지 않는다.

우선순위:

```text
1. Drive 폴더 구조
2. manifest 생성기
3. viewer-v2 manifest 렌더링
4. 워터마크 인쇄
5. bbox 좌표 매핑
6. 오답노트 생성
```

---

## 15. 개발 8대 우선순위

```text
0. 9대 category_id / subcategory_id 확정
1. Google Drive 9대 폴더 구조 생성
2. bookId 규칙 확정
3. page-001.jpg 네이밍 규칙 확정
4. manifest.json 생성기 제작
5. viewer-v2가 manifest를 읽어 페이지 표시
6. Drive fileId 표시 방식 1차 테스트
7. 인쇄용 워터마크 PDF 생성 모듈
8. 문항 bbox 좌표 매핑
```

---

## 16. 클로드 토큰 방어용 초압축 지시

클로드에게는 아래 문장만 준다.

```text
클로드, 아래 기준만 따른다.

UI는 9대 대분류 콤팩트 탭 구조.
자산 저장은 Google Drive.
webContentLink 고정 저장 금지.
각 교재는 bookId + manifest.json으로 관리.
각 페이지는 driveFileId + page-001.jpg 규칙으로 관리.
1차 파일럿은 Drive fileId 기반 임시 표시.
최종 운영은 인증/프록시 전환 가능하게 설계.
작업 범위 확장 금지.
```

---

## 17. 개발팀 전달용 최종 한 줄

```text
GFIELD-ON Archiv 파일럿은 Google Drive 원본 저장 + bookId/manifest 기반 렌더링으로 간다. webContentLink 직결은 금지하고, 1차 파일럿은 Drive fileId 임시 표시, 최종 운영은 인증/프록시 구조로 전환한다.
```

---

## 18. 현재 바로 시작해도 되는 작업

```text
1단계: Google Drive 폴더 트리 구축
4단계: manifest.json 생성기 제작
```

단, viewer의 Drive 이미지 로딩은 아래를 구분해서 설계한다.

```text
1차 파일럿 임시 표시 방식
최종 운영 인증/프록시 방식
```

---

## 19. 금지 사항

```text
webContentLink를 영구 이미지 URL로 저장 금지
외부 교재 전체 자유 다운로드 금지
워터마크 없는 인쇄 금지
문항별 이미지 대량 절단 저장 금지
실시간 웹소켓 필기 싱크 구현 금지
모바일 viewer-v2 세로 스택 강제 전환 금지
```

---

## 20. 최종 요약

```text
UI는 관제센터안.
자산 저장과 로딩은 파일럿 팀안.
Google Drive를 원본 창고로 사용.
bookId + manifest.json으로 관리.
viewer-v2는 manifest를 읽어 렌더링.
1차 파일럿은 Drive fileId 기반 임시 표시.
최종 운영은 인증/프록시 구조.
인쇄는 가능하지만 워터마크 필수.
오답노트는 통 페이지 이미지 + bbox 좌표 매핑으로 확장.
```
