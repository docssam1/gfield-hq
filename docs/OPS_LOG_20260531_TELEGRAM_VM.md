# OPS_LOG_20260531_TELEGRAM_VM

## 1. 운영 방향

GFIELD 작업은 앞으로 아래 구조를 기준으로 진행한다.

```text
GPT: 설계, 검수, 지시
Telegram Bot: 모바일 관제 명령창
Google Cloud VM: 실제 실행 서버
GitHub: 기준 저장소, 백업, 커밋 기록
Cloud Run: Gemini 프록시
Google Drive: 대용량 자료와 출력물 저장소
```

## 2. 저장소 역할

### docssam1/gfield-hq

역할: 통합 관제센터

현재 Telegram 명령:

```text
/run status
/run deploy
/run drive_scan
/run algebra2_status
/run algebra2_backup
/run algebra2_diff
/run algebra2_test
/run algebra2_clean
```

### docssam1/algebra2

역할: Algebra2 Smart Placement Hub 서비스 저장소

서비스 링크:

```text
https://docssam1.github.io/algebra2/
```

Cloud Run Health:

```text
https://algebra2-gemini-proxy-v2-274099580288.asia-northeast3.run.app/api/health
```

## 3. 기준 커밋

기존 작동 기준:

```text
50878cd10036e0e82528ed482be8946131746aba
```

인수인계 문서 추가 후 기준:

```text
1cee9487b9f63deb859b391376233527ae4502c5
```

실제 HTML 백업 생성 후 최신:

```text
bbda724
```

## 4. 생성된 고정 문서

`docssam1/algebra2`에 생성 완료:

```text
HANDOFF_ALGEBRA2.md
ROADMAP_ALGEBRA2_NEXT.md
BACKUP_AND_DEPLOY_RULES.md
```

목적:

- 새 대화창에서도 작업 기준 유지
- GPT, Codex, Gemini, 사람 작업자가 같은 기준으로 이어가기
- 로컬 PC 기준 작업 방지
- GitHub 기준 복구 경로 유지

## 5. 실제 HTML 백업 현황

VM에서 백업 후 GitHub push 완료:

```text
Commit: bbda724 Backup algebra2 index 20260531_031306
File: backups/index_base_20260531_031306.html
```

VM 상태 확인 결과:

```text
Repo: /home/gfield7265/gfield-projects/algebra2
Branch: main
Local: bbda724 Backup algebra2 index 20260531_031306
Remote main: bbda724 Backup algebra2 index 20260531_031306
Working tree: clean
```

확인된 백업 목록:

```text
backups/index_base_20260531_024934.html
backups/index_base_20260531_031146.html
backups/index_base_20260531_031306.html
backups/index_base_50878cd_BACKUP.md
```

주의:

- `.md` 파일은 설명용 포인터다.
- 실제 복구 기준은 `.html` 백업 파일과 커밋 해시다.

## 6. 해결된 문제

### VM git 작성자 정보 누락

증상:

```text
Author identity unknown
```

조치:

- `scripts/algebra2_backup.sh`에서 algebra2 저장소 내부 local git identity를 자동 설정하도록 수정
- 전역 git 설정은 건드리지 않음

### GitHub push 실패

증상:

```text
Permission denied publickey
```

조치:

- algebra2 전용 Deploy Key 등록
- write 권한 체크
- VM SSH config에 algebra2 전용 host 추가
- algebra2 origin을 SSH remote로 변경

최종 push 성공:

```text
1cee948..bbda724 main -> main
```

## 7. 다음 작업 순서

```text
Step 1. /run algebra2_diff
Step 2. /run algebra2_test
Step 3. 정상 확인 후 OMR snapshot 최소 패치 설계
Step 4. 패치 전 /run algebra2_backup
Step 5. 작은 범위 패치
Step 6. /run algebra2_diff
Step 7. /run algebra2_test
Step 8. 확인 후 push/deploy
```

## 8. 운영 금지 사항

```text
index.html 전체 재작성 금지
백업 없는 수정 금지
로컬 PC 파일 기준 작업 금지
Cloud Run 백엔드 임의 수정 금지
부모 발송 금지
운영 DB 수정 금지
Telegram 자유 shell 명령 개방 금지
```

## 9. 현재 결론

Telegram 단독 운영 1차 구조는 잡혔다.

이제부터는 VM을 직접 왕복하지 않고 가능한 한 Telegram Bot 명령으로 진행한다.
