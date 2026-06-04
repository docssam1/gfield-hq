#!/usr/bin/env bash
set -euo pipefail

cat <<'OUT'
학원 PC 연결 상태

VM: gfield-hq-vm
역할: Telegram 명령 수신 / Drive scan / inventory / 상태 확인
학원 PC 역할: eBook 이미지 변환 작업장 / 승인 / 현장 관제

현재 상태:
- Telegram -> VM: 작동 중
- VM -> 학원 PC bridge: 확인 필요
- 학원 PC agent: 로컬에서 실행 확인됨
- 허용 명령: PC핑, PC상태
OUT
