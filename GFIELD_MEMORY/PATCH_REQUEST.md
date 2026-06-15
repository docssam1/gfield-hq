# PATCH_REQUEST 워크플로우

## 역할 분담
- Claude → 이 파일(PATCH_REQUEST.md)에 변경 조각만 작성
- GPT → 대상 파일을 GitHub에서 fetch → patch 적용 → push
- Claude → 결과 확인만 (전체 파일 읽기/쓰기 금지)

## 작성 규칙
- 줄 번호 사용 금지
- 파일명 + FIND 블록 + REPLACE 블록만 작성
- FIND는 파일에서 유일하게 찾을 수 있는 최소 블록
- 직접 수정하지 않음. PATCH_REQUEST 작성 후 GPT에게 전달

## 형식

```
## 대상 파일
{repo}/{path}

## PATCH 1
FIND:
{기존 코드 블록}

REPLACE:
{새 코드 블록}
```

---

# 현재 PATCH_REQUEST

## 대상 파일
docssam1/gfield-hq → GFIELD_MEMORY/WORKER_OPERATING_RULES.md

## PATCH 1
FIND:
## 공통 작업 원칙

REPLACE:
## 파일 수정 규칙 (Claude 전용 강제 규칙)
- `get_file_contents`로 HTML/JS 등 운영 파일 전체 읽기 금지
- `create_or_update_file`로 운영 파일 전체 쓰기 금지
- GitHub에 허용된 유일한 쓰기: `GFIELD_MEMORY/PATCH_REQUEST.md` 업데이트만
- 위 규칙 위반이 필요한 경우: "전체 수정 필요. 이유: ___" 명시 후 원장님 승인 필수
- 승인 없이 전체 파일을 읽거나 쓴 경우: 작업 중단 후 보고

## 공통 작업 원칙
