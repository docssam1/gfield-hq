#!/usr/bin/env bash
set -euo pipefail

BRIDGE="${GFIELD_PC_BRIDGE_DIR:-/home/gfield7265/gfield_output/pc_bridge}"

echo "PC bridge 상태"
echo "bridge=${BRIDGE}"
echo

if [ -d "$BRIDGE" ]; then
  find "$BRIDGE" -maxdepth 2 -type f | sort | tail -20
else
  echo "bridge directory not found"
fi

echo
echo "주의: VM 로컬 bridge와 학원 PC G: Drive bridge가 같은 위치인지 확인 필요"
