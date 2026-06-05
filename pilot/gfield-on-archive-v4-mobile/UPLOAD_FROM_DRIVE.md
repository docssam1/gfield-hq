# GFIELD-ON Archive Mobile Pilot

업로드 기준일: 2026-06-05

이 폴더는 GFIELD-ON archive mobile pilot package를 기존 운영 파일과 충돌하지 않게 올리기 위한 파일럿 위치입니다.

## 원본 Google Drive 폴더

- 폴더명: `gfield_on_archive_preview_package`
- Drive 링크: https://drive.google.com/drive/folders/1D-kTQlv8IMzPNwbk7whkf4yIyh73NBok

## GitHub 반영 위치

최종 파일은 아래 위치에 배치합니다.

```text
pilot/gfield-on-archive-v4-mobile/
```

## 확인된 핵심 파일

```text
gfield-on-archive-preview.html
gfield-on-archive-admin.html
books/hs-thinking-basic/viewer.html
books/hs-thinking-basic/source.html
assets/gfield-on-dashboard.jpg.png
assets/gfield-on-intro.mp4
assets/gfield-on-poster.jpg
assets/gfield-logo.png
```

## 원본 폴더 내 확인된 구조

```text
gfield_on_archive_preview_package/
├─ books/
│  └─ hs-thinking-basic/
│     ├─ viewer.html
│     └─ source.html
├─ assets/
│  ├─ gfield-on-dashboard.jpg.png
│  ├─ gfield-on-intro.mp4
│  ├─ gfield-on-poster.jpg
│  └─ gfield-logo.png
├─ gfield-on-archive-preview.html
├─ gfield-on-archive-admin.html
├─ GFIELD_ON_사용설명서_2026-06-05.md
├─ GFIELD_ON_현재기준_정리_2026-06-05.md
├─ GFIELD_ON_광고문구_정리.txt
├─ gfield-on-archive-preview.backup-2026-06-04-stage2.html
├─ gfield-on-archive-preview.before-ai-modal.html
└─ README.txt
```

## 업로드 원칙

- 운영 루트에 바로 넣지 않습니다.
- 기존 pilot 또는 운영 파일을 덮어쓰지 않습니다.
- 전체 폴더 구조를 유지합니다.
- HTML 파일 4개만 올리면 화면 일부가 깨질 수 있으므로 assets까지 함께 반영합니다.
- 현재 버전은 데모/파일럿 기준입니다.
- 책장 넘김은 기본 구현 상태로 유지합니다.

## GitHub Pages 확인 경로

저장소가 GitHub Pages로 `main` 브랜치 루트를 배포 중이면 아래 경로로 확인합니다.

```text
https://docssam1.github.io/gfield-hq/pilot/gfield-on-archive-v4-mobile/gfield-on-archive-preview.html
https://docssam1.github.io/gfield-hq/pilot/gfield-on-archive-v4-mobile/gfield-on-archive-admin.html
https://docssam1.github.io/gfield-hq/pilot/gfield-on-archive-v4-mobile/books/hs-thinking-basic/viewer.html
https://docssam1.github.io/gfield-hq/pilot/gfield-on-archive-v4-mobile/books/hs-thinking-basic/source.html
```

## 현재 처리 상태

- Drive 폴더 접근 확인 완료
- GitHub 저장소 `docssam1/gfield-hq` 접근 및 push 권한 확인 완료
- 이 파일은 파일럿 업로드 위치를 먼저 고정하기 위해 생성함
- 남은 작업: Drive 폴더 전체 파일을 이 경로로 복사 업로드

## 주의

현재 ChatGPT GitHub 커넥터는 UTF-8 텍스트 파일 생성/수정 중심입니다. `assets`의 PNG/MP4 같은 바이너리 파일은 GitHub 웹 업로드, GitHub Desktop, `git` 명령, 또는 Codex/로컬 스크립트로 업로드해야 합니다.
