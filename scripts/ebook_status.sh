#!/usr/bin/env bash
set -euo pipefail

cat <<'OUT'
G.FIELD ON eBook 상태

1차 원칙:
- OCR 자동화 아님
- PDF/HWP/HWPX를 페이지 이미지(JPG/WebP)로 변환
- 학원 PC가 변환 작업장
- VM은 Telegram, Drive scan, inventory, 상태 확인 담당
- GitHub Pages viewer는 manifest.json + 상대경로 이미지 기준

현재 보류:
- OCR 자동 추출
- PaddleOCR 대량 처리
- Cloud Run Job
- Drive embed
- 학생별 민감 자료 실시간 권한 제어

확인 필요:
- Drive 변환 결과 루트 경로
- books/{book_id}/manifest.json 실제 산출물 위치
- materials.json / manifest.json GitHub Pages 연결 경로
OUT
