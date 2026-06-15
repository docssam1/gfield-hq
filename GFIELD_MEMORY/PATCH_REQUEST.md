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

## PATCH 2
FIND:
...

REPLACE:
...
```

---

# 현재 PATCH_REQUEST

(작업 없음)
