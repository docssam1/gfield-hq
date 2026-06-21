#!/usr/bin/env python3
"""
PDF 손글씨 제거 스크립트
Gemini Flash 2.0 Vision으로 손글씨 좌표 감지 → PIL로 흰색 마스킹 → PDF 재합본

사용법:
  python pdf_eraser.py input.pdf
  python pdf_eraser.py input.pdf --dpi 200 --output output/result.pdf

설치:
  pip install pdf2image pillow google-generativeai --break-system-packages
  sudo apt-get install -y poppler-utils
"""

import os
import sys
import json
import time
import argparse
import re
from pathlib import Path
from PIL import Image, ImageDraw
from pdf2image import convert_from_path
import google.generativeai as genai

# ── 설정 ──────────────────────────────────────────────
GEMINI_MODEL = "gemini-2.0-flash"
DPI = 200
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds (무료 티어 rate limit 대비)
# ────────────────────────────────────────────────────────


def setup_gemini():
    """Gemini API 초기화 (GOOGLE_API_KEY 또는 ADC 방식)"""
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)
        print(f"[AUTH] API Key 방식으로 인증")
    else:
        # Application Default Credentials (gfield-drive-worker.json)
        print(f"[AUTH] ADC 방식으로 인증 (GOOGLE_APPLICATION_CREDENTIALS)")
    return genai.GenerativeModel(GEMINI_MODEL)


def detect_handwriting(model, image: Image.Image, page_num: int) -> list[dict]:
    """Gemini로 손글씨 영역 좌표 감지"""
    w, h = image.size
    prompt = f"""이 이미지에서 손으로 쓴 글씨, 채점 표시(동그라미, 체크, 숫자 답안), 필기 메모 등
손글씨로 보이는 모든 영역의 좌표를 JSON으로 반환하세요.

이미지 크기: {w}x{h}px

규칙:
- 인쇄된 글씨(컴퓨터 폰트)는 절대 포함하지 마세요
- 손글씨, 볼펜/연필로 쓴 것만 포함하세요
- 여백을 조금 넉넉히 잡아주세요 (실제보다 5~10px 크게)

다음 JSON 형식으로만 응답하세요 (마크다운, 설명 없이 순수 JSON만):
{{"regions": [{{"x": 숫자, "y": 숫자, "w": 숫자, "h": 숫자, "desc": "설명"}}]}}

손글씨가 없으면: {{"regions": []}}"""

    for attempt in range(MAX_RETRIES):
        try:
            response = model.generate_content([prompt, image])
            text = response.text.strip()
            # JSON 추출 (```json ... ``` 감싸인 경우 처리)
            text = re.sub(r"```json\s*|\s*```", "", text).strip()
            parsed = json.loads(text)
            regions = parsed.get("regions", [])
            print(f"  [페이지 {page_num}] {len(regions)}개 손글씨 영역 감지")
            return regions
        except json.JSONDecodeError as e:
            print(f"  [페이지 {page_num}] JSON 파싱 오류 (시도 {attempt+1}/{MAX_RETRIES}): {e}")
            print(f"  응답: {text[:200]}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
        except Exception as e:
            print(f"  [페이지 {page_num}] API 오류 (시도 {attempt+1}/{MAX_RETRIES}): {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)

    print(f"  [페이지 {page_num}] 감지 실패 — 이 페이지는 원본 유지")
    return []


def erase_regions(image: Image.Image, regions: list[dict]) -> Image.Image:
    """감지된 영역을 흰색으로 마스킹"""
    if not regions:
        return image
    img = image.copy()
    draw = ImageDraw.Draw(img)
    for r in regions:
        x, y, w, h = int(r["x"]), int(r["y"]), int(r["w"]), int(r["h"])
        # 여백 5px 추가
        draw.rectangle([x - 5, y - 5, x + w + 5, y + h + 5], fill="white")
    return img


def process_pdf(input_path: str, output_path: str, dpi: int = DPI):
    input_path = Path(input_path)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*50}")
    print(f"입력: {input_path.name}")
    print(f"출력: {output_path}")
    print(f"DPI: {dpi}")
    print(f"모델: {GEMINI_MODEL}")
    print(f"{'='*50}\n")

    # 1. Gemini 초기화
    model = setup_gemini()

    # 2. PDF → 이미지 변환
    print(f"[1/3] PDF를 이미지로 변환 중 (DPI={dpi})...")
    pages = convert_from_path(str(input_path), dpi=dpi)
    total = len(pages)
    print(f"  총 {total}페이지 변환 완료\n")

    # 3. 페이지별 손글씨 감지 + 마스킹
    print(f"[2/3] 페이지별 손글씨 감지 중...")
    cleaned_pages = []
    for i, page_img in enumerate(pages, 1):
        print(f"  [{i}/{total}] 분석 중...", end=" ")
        regions = detect_handwriting(model, page_img, i)
        cleaned = erase_regions(page_img, regions)
        cleaned_pages.append(cleaned)
        # 무료 티어 rate limit 대비 (15 req/min)
        if i % 14 == 0 and i < total:
            print(f"  Rate limit 대비 대기 중 (60초)...")
            time.sleep(60)
        else:
            time.sleep(1)

    # 4. PDF 재합본
    print(f"\n[3/3] PDF 재합본 중...")
    first = cleaned_pages[0].convert("RGB")
    rest = [p.convert("RGB") for p in cleaned_pages[1:]]
    first.save(str(output_path), save_all=True, append_images=rest, resolution=dpi)
    print(f"\n완료! → {output_path}")
    print(f"파일 크기: {output_path.stat().st_size / 1024 / 1024:.1f} MB")


def main():
    parser = argparse.ArgumentParser(description="PDF 손글씨 제거 (Gemini Flash 2.0)")
    parser.add_argument("input", help="입력 PDF 파일 경로")
    parser.add_argument("--dpi", type=int, default=DPI, help=f"렌더링 DPI (기본: {DPI})")
    parser.add_argument("--output", help="출력 PDF 경로 (기본: output/입력파일명_cleaned.pdf)")
    args = parser.parse_args()

    if not Path(args.input).exists():
        print(f"오류: 파일을 찾을 수 없습니다 → {args.input}")
        sys.exit(1)

    if args.output:
        output_path = args.output
    else:
        stem = Path(args.input).stem
        output_path = f"output/{stem}_cleaned.pdf"

    process_pdf(args.input, output_path, args.dpi)


if __name__ == "__main__":
    main()
