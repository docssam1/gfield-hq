#!/usr/bin/env bash
set -euo pipefail

cat <<'CMDS'
=== GFIELD TELEGRAM COMMANDS ===

[HQ]
/run status
/run deploy
/run deploy_safe
/run hq_status
/run hq_rebase
/run hq_commands

[Drive]
/run drive_scan
/run 카톡정리
/run 리포트정리
/run 리포트상태

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

[Short aliases]
/run hq
/run safe
/run commands
/run a2
/run a2_backup
/run a2_diff
/run a2_test
/run a2_clean

[Korean aliases]
/run 상태
/run 목록
/run 동기화
/run 복구
CMDS
