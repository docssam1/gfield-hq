#!/usr/bin/env bash
set -euo pipefail

cat <<'OUT'
PC핑 요청 수신됨.

현재 VM은 Telegram 명령을 받았고, 학원 PC agent는 별도 bridge로 대기 중입니다.
상태: PC bridge 연결 확인 필요
허용 작업: ping/status only
금지 작업: 파일 변경, 삭제, 전송, 자동 실행
OUT
