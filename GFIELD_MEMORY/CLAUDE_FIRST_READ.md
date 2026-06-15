# CLAUDE_FIRST_READ.md
# 새 채팅창 시작 시 반드시 이 내용을 첫 메시지에 붙여넣으세요

---

## 복붙용 세션 시작 템플릿

```
이 프로젝트는 GFIELD 작업입니다.

먼저 아래 공통 원칙 문서를 읽고 시작하세요:

GitHub:
- docssam1/gfield-hq → GFIELD_MEMORY/WORKER_OPERATING_RULES.md
- docssam1/gfield-hq → GFIELD_MEMORY/PATCH_REQUEST.md

작업 규칙 (위반 시 즉시 중단):
- 운영 파일 전체 읽기 금지 (get_file_contents로 HTML/JS 등 대용량 파일 읽기 금지)
- 운영 파일 전체 쓰기 금지 (create_or_update_file로 직접 push 금지)
- GitHub 허용 쓰기: GFIELD_MEMORY/PATCH_REQUEST.md 단 1개만
- 전체 수정이 꼭 필요하면: "전체 수정 필요. 이유: ___" 보고 후 승인 받을 것
- 작업 전 계획 보고 → 승인 후 실행
```

---

## 주요 경로 상수 (매번 찾지 말고 여기서 복붙)

| 항목 | 값 |
|------|-----|
| WORKER_OPERATING_RULES | docssam1/gfield-hq → GFIELD_MEMORY/WORKER_OPERATING_RULES.md |
| PATCH_REQUEST | docssam1/gfield-hq → GFIELD_MEMORY/PATCH_REQUEST.md |
| GFIELD_MEMORY 폴더 ID (Drive) | 1JN87A1S0XUziE1Ggyb_bu8lAq5ioXe5L |
| hyper-focus 운영본 | docssam1/lete-on → hyper-focus/index.html |
| hyper-focus URL | https://docssam1.github.io/lete-on/hyper-focus/ |
| Apps Script URL | https://script.google.com/macros/s/AKfycbzwtu2FOu_rmqT-pyhwakl0EYrkbdUHUwTYnxB0GBlLcZlgXqmxTJfObeKQHx8Tu_FZsA/exec |
| 승인번호 포함 문자열 | 777200 |

---

## GPT에게 PATCH 적용 요청할 때

```
GFIELD_MEMORY/PATCH_REQUEST.md 읽고
[대상 파일]에 PATCH 적용해줘

GitHub: docssam1/gfield-hq
```
