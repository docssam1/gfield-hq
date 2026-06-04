#!/usr/bin/env bash
set -euo pipefail

cat <<'CMDS'
=== GFIELD 텔레그램 명령어 ===

[HQ]
/run status
/run deploy
/run deploy_safe
/run hq_status
/run hq_rebase
/run hq_commands

[Drive / Report]
/run drive_scan
/run 카톡정리
/run 리포트정리
/run 리포트상태

[학원 PC 연결]
/run PC핑
/run PC상태
/run PC목록
/run PC결과

[G.FIELD ON / eBook]
/run 이북상태
/run eBook상태
/run ebook_status

[Algebra2]
/run algebra2_status
/run algebra2_backup
/run algebra2_diff
/run algebra2_test
/run algebra2_clean
/run algebra2_patch_omr
/run algebra2_patch_materials
/run algebra2_patch_omr_layout
/run algebra2_patch_answer_matrix

[Algebra2 한글]
/run 알지상태
/run 알지백업
/run 알지확인
/run 알지검사
/run 알지정리
/run 정오답패치
/run 오엠알패치
/run 교재패치

[짧은 별명]
/run hq
/run safe
/run commands
/run a2
/run a2_backup
/run a2_diff
/run a2_test
/run a2_clean

[한글 별명]
/run 상태
/run 목록
/run 동기화
/run 복구
/run 카톡정리
/run 리포트정리
/run 리포트상태
/run PC핑
/run PC상태
/run 이북상태

현재 정책:
- 학원 PC 명령은 ping/status 확인만 허용
- 파일 변경/삭제/전송 명령은 금지
- eBook 1차는 학원 PC 변환 작업장 기준
- VM은 Telegram/Drive inventory/상태 확인 담당
CMDS
