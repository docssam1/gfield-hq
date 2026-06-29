#!/usr/bin/env python3
"""
smart_eraser.py
pix2text 레이아웃 분석 + Gemini Vision (Vertex AI) 으로 손글씨만 골라서 흰색 마스킹

사용법:
  python3 smart_eraser.py input.jpg
  python3 smart_eraser.py input.jpg --output output/result.png

인증:
  gcloud auth application-default login
  gcloud config set project gen-lang-client-0794247388
"""

import os
import sys
import json
import base64
import argparse
from pathlib import Path
from PIL import Image, ImageDraw
import google.auth
import google.auth.transport.requests
import requests


PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "gen-lang-client-0794247388")
LOCATION = "us-central1"
MODEL = "gemini-2.5-flash"


def get_access_token() -> str:
    """Vertex AI ADC 인증 토큰 획득"""
    creds, _ = google.auth.default(
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    creds.refresh(google.auth.transport.requests.Request())
    return creds.token


def call_gemini_vertex(prompt: str, image: Image.Image) -> str:
    """Vertex AI REST API로 Gemini 호출"""
    import io
    buf = io.BytesIO()
    image.save(buf, format="JPEG", quality=85)
    img_b64 = base64.b64encode(buf.getvalue()).decode()

    token = get_access_token()
    url = (
        f"https://{LOCATION}-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}"
        f"/locations/{LOCATION}/publishers/google/models/{MODEL}:generateContent"
    )
    payload = {
        "contents": [{
            "role": "user",
            "parts": [
                {"inlineData": {"mimeType": "image/jpeg", "data": img_b64}},
                {"text": prompt}
            ]
        }],
        "generationConfig": {"temperature": 0, "maxOutputTokens": 1024}
    }
    resp = requests.post(
        url,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json=payload,
        timeout=60
    )
    resp.raise_for_status()
    return resp.json()["candidates"][0]["content"]["parts"][0]["text"]


def get_layout(image_path: str) -> list:
    """pix2text로 레이아웃 분석"""
    from pix2text import Pix2Text
    p2t = Pix2Text.from_config()
    output_dir = Path(image_path).parent / "pix2text_tmp"
    output_dir.mkdir(exist_ok=True)
    p2t.recognize_page(image_path, save_debug_res=str(output_dir))
    json_path = output_dir / "layout_out.json"
    if json_path.exists():
        with open(json_path) as f:
            return json.load(f)
    return []


def classify_regions(image: Image.Image, regions: list) -> list:
    """Gemini Vision으로 손글씨 영역 분류"""
    if not regions:
        return []

    region_desc = []
    for i, r in enumerate(regions):
        pos = r["position"]
        x1 = min(p[0] for p in pos)
        y1 = min(p[1] for p in pos)
        x2 = max(p[0] for p in pos)
        y2 = max(p[1] for p in pos)
        region_desc.append({
            "id": i,
            "type": r["type"],
            "box": [round(x1), round(y1), round(x2), round(y2)],
            "score": round(r["score"], 2)
        })

    prompt = f"""이 시험지 이미지에서 각 영역이 손글씨인지 인쇄된 것인지 분류해주세요.

영역 목록:
{json.dumps(region_desc, ensure_ascii=False, indent=2)}

다음 JSON 형식으로만 응답하세요 (마크다운 없이 순수 JSON):
{{"handwriting": [손글씨인 id 목록], "printed": [인쇄된 것 id 목록]}}

판단 기준:
- 손글씨: 학생이 쓴 답안, 계산 과정, 동그라미 채점 표시, 낙서, 필기
- 인쇄: 문제 번호, 문제 텍스트, 인쇄된 도형/그림, 표
- 확실하지 않으면 printed로 분류 (인쇄 텍스트 보호 우선)"""

    text = call_gemini_vertex(prompt, image)
    text = text.replace("```json", "").replace("```", "").strip()
    result = json.loads(text)
    return result.get("handwriting", [])


def erase_handwriting(image: Image.Image, regions: list, handwriting_ids: list) -> Image.Image:
    """손글씨 영역 흰색 마스킹"""
    img = image.copy()
    draw = ImageDraw.Draw(img)
    erased = 0
    for i, r in enumerate(regions):
        if i not in handwriting_ids:
            continue
        pos = r["position"]
        x1 = min(p[0] for p in pos)
        y1 = min(p[1] for p in pos)
        x2 = max(p[0] for p in pos)
        y2 = max(p[1] for p in pos)
        draw.rectangle([x1-5, y1-5, x2+5, y2+5], fill="white")
        erased += 1
        print(f"  지움: 영역 {i} ({r['type']}) [{round(x1)},{round(y1)},{round(x2)},{round(y2)}]")
    print(f"총 {erased}개 손글씨 영역 제거 완료")
    return img


def process(input_path: str, output_path: str = None):
    inp = Path(input_path)
    if not output_path:
        out = inp.parent / "output" / f"{inp.stem}_cleaned{inp.suffix}"
    else:
        out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    print(f"\n입력: {inp.name}")
    print(f"출력: {out}")
    print(f"프로젝트: {PROJECT_ID} / {LOCATION}")

    print("\n[1/3] pix2text 레이아웃 분석 중...")
    regions = get_layout(str(inp))
    print(f"  {len(regions)}개 영역 감지 (FIGURE:{sum(1 for r in regions if r['type']=='FIGURE')}, TEXT:{sum(1 for r in regions if r['type']=='TEXT')}, TITLE:{sum(1 for r in regions if r['type']=='TITLE')})")

    print("\n[2/3] Gemini Vision (Vertex AI)으로 손글씨 분류 중...")
    image = Image.open(inp).convert("RGB")
    handwriting_ids = classify_regions(image, regions)
    print(f"  손글씨로 분류된 영역: {handwriting_ids}")

    print("\n[3/3] 손글씨 영역 마스킹 중...")
    result = erase_handwriting(image, regions, handwriting_ids)
    result.save(str(out))
    print(f"\n완료! → {out}")


def main():
    parser = argparse.ArgumentParser(description="스마트 손글씨 제거 (pix2text + Gemini Vertex AI)")
    parser.add_argument("input", help="입력 이미지 (JPG/PNG)")
    parser.add_argument("--output", help="출력 경로")
    parser.add_argument("--project", help=f"GCP 프로젝트 ID (기본: {PROJECT_ID})")
    args = parser.parse_args()
    if args.project:
        global PROJECT_ID
        PROJECT_ID = args.project
    process(args.input, args.output)


if __name__ == "__main__":
    main()
