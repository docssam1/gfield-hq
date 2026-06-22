#!/usr/bin/env python3
"""
PDF/이미지 손글씨 제거 스크립트
Gemini Flash 2.0 Vision으로 손글씨 좌표 감지 → PIL로 흰색 마스킹 → PDF/이미지 저장

사용법:
  python pdf_eraser.py input.pdf
  python pdf_eraser.py input.jpg
  python pdf_eraser.py input.png --output output/result.png

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
import google.generativeai as genai

GEMINI_MODEL = "gemini-2.0-flash"
DPI = 200
MAX_RETRIES = 3
RETRY_DELAY = 5
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"}


def setup_gemini():
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)
        print("[AUTH] API Key 방식으로 인증")
    else:
        print("[AUTH] ADC 방식으로 인증 (GOOGLE_APPLICATION_CREDENTIALS)")
    return genai.GenerativeModel(GEMINI_MODEL)


def detect_handwriting(model, image: Image.Image, page_num: int) -> list:
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
            text = re.sub(r"```json\s*|\s*```", "", response.text.strip()).strip()
            parsed = json.loads(text)
            regions = parsed.get("regions", [])
            print(f"  [{page_num}페이지] {len(regions)}개 손글씨 영역 감지")
            return regions
        except json.JSONDecodeError as e:
            print(f"  [{page_num}페이지] JSON 파싱 오류 (시도 {attempt+1}/{MAX_RETRIES}): {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
        except Exception as e:
            print(f"  [{page_num}페이지] API 오류 (시도 {attempt+1}/{MAX_RETRIES}): {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)

    print(f"  [{page_num}페이지] 감지 실패 — 원본 유지")
    return []


def erase_regions(image: Image.Image, regions: list) -> Image.Image:
    if not regions:
        return image
    img = image.copy()
    draw = ImageDraw.Draw(img)
    for r in regions:
        x, y, w, h = int(r["x"]), int(r["y"]), int(r["w"]), int(r["h"])
        draw.rectangle([x - 5, y - 5, x + w + 5, y + h + 5], fill="white")
    return img


def load_pages(input_path: Path, dpi: int) -> list:
    ext = input_path.suffix.lower()
    if ext == ".pdf":
        from pdf2image import convert_from_path
        print(f"[1/3] PDF → 이미지 변환 중 (DPI={dpi})...")
        pages = convert_from_path(str(input_path), dpi=dpi)
        print(f"  총 {len(pages)}페이지 변환 완료\n")
        return pages
    elif ext in IMAGE_EXTS:
        print(f"[1/3] 이미지 로드 중...")
        img = Image.open(input_path).convert("RGB")
        print(f"  크기: {img.size[0]}x{img.size[1]}px\n")
        return [img]
    else:
        print(f"오류: 지원하지 않는 형식 ({ext})")
        sys.exit(1)


def save_output(pages: list, output_path: Path, dpi: int, is_image: bool):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if is_image:
        pages[0].convert("RGB").save(str(output_path))
    else:
        first = pages[0].convert("RGB")
        rest = [p.convert("RGB") for p in pages[1:]]
        first.save(str(output_path), save_all=True, append_images=rest, resolution=dpi)
    print(f"\n완료! → {output_path}")
    print(f"파일 크기: {output_path.stat().st_size / 1024 / 1024:.1f} MB")


def process(input_path: str, output_path: str, dpi: int = DPI):
    inp = Path(input_path)
    is_image = inp.suffix.lower() in IMAGE_EXTS

    # 출력 경로 자동 설정
    if not output_path:
        suffix = inp.suffix if is_image else ".pdf"
        output_path = f"output/{inp.stem}_cleaned{suffix}"
    out = Path(output_path)

    print(f"\n{'='*50}")
    print(f"입력: {inp.name}  ({'이미지' if is_image else 'PDF'})")
    print(f"출력: {out}")
    print(f"모델: {GEMINI_MODEL}")
    print(f"{'='*50}\n")

    model = setup_gemini()
    pages = load_pages(inp, dpi)
    total = len(pages)

    print(f"[2/3] 손글씨 감지 중...")
    cleaned = []
    for i, page_img in enumerate(pages, 1):
        print(f"  [{i}/{total}] 분석 중...", end=" ")
        regions = detect_handwriting(model, page_img, i)
        cleaned.append(erase_regions(page_img, regions))
        if i % 14 == 0 and i < total:
            print("  Rate limit 대기 (60초)...")
            time.sleep(60)
        elif i < total:
            time.sleep(1)

    print(f"\n[3/3] 저장 중...")
    save_output(cleaned, out, dpi, is_image)


def main():
    parser = argparse.ArgumentParser(description="PDF/이미지 손글씨 제거 (Gemini Flash 2.0)")
    parser.add_argument("input", help="입력 파일 (PDF, JPG, PNG 등)")
    parser.add_argument("--dpi", type=int, default=DPI, help=f"PDF 렌더링 DPI (기본: {DPI})")
    parser.add_argument("--output", help="출력 파일 경로")
    args = parser.parse_args()

    if not Path(args.input).exists():
        print(f"오류: 파일을 찾을 수 없습니다 → {args.input}")
        sys.exit(1)

    process(args.input, args.output, args.dpi)


if __name__ == "__main__":
    main()
