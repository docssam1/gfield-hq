# TASK: STORE_URL 교체 (roadmap/index.html 1곳만)

## 무엇을 / 왜
G-FIELD 로드맵 저장 서버(Apps Script)가 새 버전으로 재배포되며 URL이 바뀌었습니다.
admin.html은 이미 새 URL로 수정·push 완료. **roadmap/index.html도 같은 URL로 맞춰야** 학부모 저장/불러오기가 정상 작동합니다.

(주의: demo/index.html에는 STORE_URL이 아예 없음 — 저장 기능 없는 미리보기 버전. 건드릴 필요 없음.)

## 대상 파일 (repo: docssam1/lete-on)
- `roadmap/index.html` (578번째 줄 근처)

## 수정 내용

**찾을 문자열 (옛 URL):**
```
https://script.google.com/macros/s/AKfycbyX98qS-UA4K82D9r1EDp5cOJw1ZuohQqW-2e7kTL_8GiRirCJeek5mwmbp3om4s7Oy/exec
```

**바꿀 문자열 (새 URL):**
```
https://script.google.com/macros/s/AKfycbwg35Q9Sd3orf5P3tJTRRXhjDYZVjbHyg_5MJVR7I30AGnoeN2ITQgiihj16fL0dXfq/exec
```

코드 형태:
```js
const STORE_URL = 'https://script.google.com/macros/s/AKfycbyX98qS-UA4K82D9r1EDp5cOJw1ZuohQqW-2e7kTL_8GiRirCJeek5mwmbp3om4s7Oy/exec';
```
↓ 이렇게만 교체:
```js
const STORE_URL = 'https://script.google.com/macros/s/AKfycbwg35Q9Sd3orf5P3tJTRRXhjDYZVjbHyg_5MJVR7I30AGnoeN2ITQgiihj16fL0dXfq/exec';
```

## 작업 방법
1. GitHub에서 `roadmap/index.html` fetch
2. 옛 URL 문자열을 새 URL로 **단순 치환** (그 줄 외 다른 곳 절대 건드리지 말 것)
3. push (커밋: `fix(store): Apps Script 재배포 URL 갱신`)

## 주의
- 파일 전체를 다시 만들지 말 것. 딱 이 URL 문자열 하나만 치환.
- 옛 URL이 **정확히 1곳**만 있어야 정상 (있는지 먼저 grep으로 확인 후 교체 권장).
- 치환 후 JS 문법 깨지지 않았는지 (따옴표·세미콜론 그대로 유지) 확인.
- demo/index.html은 작업 대상 아님.
