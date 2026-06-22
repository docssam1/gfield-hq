#!/usr/bin/env python3
"""
Single-file document cleaner for worksheet and scan restoration.

Features:
- PDF or image input
- Document boundary detection and perspective correction
- Background whitening and contrast enhancement
- Color-preserving, scan-style, or strong black-and-white output
- Conservative handwriting attenuation
"""

from __future__ import annotations

import argparse
import io
import json
import os
import sys
import time
from pathlib import Path

import cv2
import google.genai as genai
import numpy as np
from PIL import Image
from pdf2image import convert_from_path
from google.genai import types

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


STYLE_COLOR = "color"
STYLE_SCAN = "scan"
STYLE_BW = "bw"

HANDWRITING_KEEP = "keep"
HANDWRITING_SOFTEN = "soften"

RESTORATION_MODE_FAST = "fast"
RESTORATION_MODE_PRECISE = "precise"

DOCUMENT_MODE_AUTO = "auto"
DOCUMENT_MODE_EXAM = "exam"
DOCUMENT_MODE_BOOK = "book"

API_RESCUE_OFF = "off"
API_RESCUE_AUTO = "auto"
API_RESCUE_ON = "on"


def log(step: str, message: str) -> None:
    print(f"[{step}] {message}", flush=True)


def describe_restoration_mode(restoration_mode: str) -> str:
    labels = {
        RESTORATION_MODE_FAST: "빠른 정리",
        RESTORATION_MODE_PRECISE: "정밀 복원",
    }
    return labels.get(restoration_mode, restoration_mode)


def pil_to_bgr(image: Image.Image) -> np.ndarray:
    rgb = image.convert("RGB")
    return cv2.cvtColor(np.array(rgb), cv2.COLOR_RGB2BGR)


def bgr_to_pil(image: np.ndarray) -> Image.Image:
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return Image.fromarray(rgb)


def bgr_to_part(image: np.ndarray) -> types.Part:
    pil_image = bgr_to_pil(image)
    buffer = io.BytesIO()
    pil_image.save(buffer, format="PNG")
    return types.Part.from_bytes(data=buffer.getvalue(), mime_type="image/png")


def order_points(pts: np.ndarray) -> np.ndarray:
    rect = np.zeros((4, 2), dtype=np.float32)
    s = pts.sum(axis=1)
    diff = np.diff(pts, axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect


def four_point_transform(image: np.ndarray, pts: np.ndarray) -> np.ndarray:
    rect = order_points(pts.astype(np.float32))
    tl, tr, br, bl = rect

    width_a = np.linalg.norm(br - bl)
    width_b = np.linalg.norm(tr - tl)
    max_width = max(int(width_a), int(width_b))

    height_a = np.linalg.norm(tr - br)
    height_b = np.linalg.norm(tl - bl)
    max_height = max(int(height_a), int(height_b))

    if max_width < 50 or max_height < 50:
        return image

    dst = np.array(
        [
            [0, 0],
            [max_width - 1, 0],
            [max_width - 1, max_height - 1],
            [0, max_height - 1],
        ],
        dtype=np.float32,
    )

    matrix = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(
        image,
        matrix,
        (max_width, max_height),
        flags=cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_REPLICATE,
    )
    return warped


def detect_document(image: np.ndarray) -> np.ndarray | None:
    height, width = image.shape[:2]
    scale = 1400.0 / max(height, width) if max(height, width) > 1400 else 1.0
    preview = cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA) if scale != 1.0 else image.copy()

    gray = cv2.cvtColor(preview, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 60, 180)
    edges = cv2.dilate(edges, np.ones((5, 5), np.uint8), iterations=2)
    edges = cv2.erode(edges, np.ones((3, 3), np.uint8), iterations=1)

    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    image_area = preview.shape[0] * preview.shape[1]

    for contour in contours[:12]:
        area = cv2.contourArea(contour)
        if area < image_area * 0.2:
            continue
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
        if len(approx) == 4:
            points = approx.reshape(4, 2).astype(np.float32) / scale
            return points

    return None


def normalize_gray(gray: np.ndarray, clip_limit: float = 2.8) -> np.ndarray:
    background = cv2.GaussianBlur(gray, (0, 0), 41)
    normalized = cv2.divide(gray, background, scale=255)
    normalized = cv2.normalize(normalized, None, 0, 255, cv2.NORM_MINMAX)
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(8, 8))
    enhanced = clahe.apply(normalized)
    return enhanced


def protect_text_denoise(gray: np.ndarray, denoise_strength: int = 18) -> tuple[np.ndarray, np.ndarray]:
    text_mask = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        41,
        15,
    )
    text_mask = cv2.morphologyEx(text_mask, cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
    text_mask = cv2.dilate(text_mask, np.ones((3, 3), np.uint8), iterations=1)

    denoised = cv2.fastNlMeansDenoising(gray, None, denoise_strength, 7, 21)
    cleaned = np.where(text_mask > 0, gray, denoised).astype(np.uint8)
    return cleaned, text_mask


def build_handwriting_mask(gray: np.ndarray, text_mask: np.ndarray) -> np.ndarray:
    inv = cv2.threshold(gray, 175, 255, cv2.THRESH_BINARY_INV)[1]
    inv = cv2.morphologyEx(inv, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8), iterations=1)

    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(inv, 8, cv2.CV_32S)
    mark_mask = np.zeros_like(gray)
    page_area = gray.shape[0] * gray.shape[1]

    for idx in range(1, num_labels):
        x, y, w, h, area = stats[idx]
        if area < 120:
            continue
        if area > page_area * 0.2:
            continue

        extent = area / max(w * h, 1)
        aspect = max(w, h) / max(min(w, h), 1)
        max_dim = max(w, h)
        bbox_mask = text_mask[y : y + h, x : x + w]
        overlap = np.count_nonzero(bbox_mask) / max(area, 1)

        if overlap > 0.92 and max_dim < 45:
            continue

        if (
            max_dim >= 42
            or area >= 260
            or extent < 0.34
            or aspect > 6.5
            or (overlap < 0.75 and max_dim >= 28)
        ):
            mark_mask[labels == idx] = 255

    mark_mask = cv2.dilate(mark_mask, np.ones((5, 5), np.uint8), iterations=1)
    mark_mask = cv2.GaussianBlur(mark_mask, (0, 0), 2)
    return mark_mask


def build_large_mark_mask(gray: np.ndarray, text_mask: np.ndarray) -> np.ndarray:
    edges = cv2.Canny(gray, 40, 140)
    edges = cv2.dilate(edges, np.ones((3, 3), np.uint8), iterations=1)

    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(edges, 8, cv2.CV_32S)
    large_mask = np.zeros_like(gray)
    page_area = gray.shape[0] * gray.shape[1]

    for idx in range(1, num_labels):
        x, y, w, h, area = stats[idx]
        if area < 140:
            continue
        if area > page_area * 0.18:
            continue

        max_dim = max(w, h)
        min_dim = max(min(w, h), 1)
        aspect = max_dim / min_dim
        bbox_text = text_mask[y : y + h, x : x + w]
        text_density = np.count_nonzero(bbox_text) / max(w * h, 1)

        if max_dim >= 70 and text_density < 0.22:
            large_mask[labels == idx] = 255
            continue

        if max_dim >= 90 and aspect > 2.0 and text_density < 0.16:
            large_mask[labels == idx] = 255

    large_mask = cv2.morphologyEx(large_mask, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8), iterations=1)
    large_mask = cv2.dilate(large_mask, np.ones((7, 7), np.uint8), iterations=1)
    return large_mask


def suppress_marks_for_bw(gray: np.ndarray, text_mask: np.ndarray, strength: float = 0.98) -> np.ndarray:
    mark_mask = build_handwriting_mask(gray, text_mask)
    large_mask = build_large_mark_mask(gray, text_mask)
    mark_mask = np.maximum(mark_mask, large_mask)
    if not np.any(mark_mask):
        return gray

    mask = (mark_mask > 24).astype(np.uint8) * 255
    mask = cv2.dilate(mask, np.ones((7, 7), np.uint8), iterations=1)

    protected_text = cv2.dilate(text_mask, np.ones((3, 3), np.uint8), iterations=2)
    removal_mask = np.where(protected_text > 0, 0, mask).astype(np.uint8)

    lifted = gray.astype(np.float32)
    removal_strength = cv2.GaussianBlur(removal_mask, (0, 0), 4).astype(np.float32) / 255.0
    lifted = lifted + (255.0 - lifted) * removal_strength * strength
    return np.clip(lifted, 0, 255).astype(np.uint8)


def analyze_page_profile(gray: np.ndarray, text_mask: np.ndarray) -> dict[str, float]:
    area = float(gray.shape[0] * gray.shape[1])
    ink_mask = cv2.threshold(gray, 182, 255, cv2.THRESH_BINARY_INV)[1]
    edge_mask = cv2.Canny(gray, 40, 140)
    handwriting_mask = build_handwriting_mask(gray, text_mask)
    large_mark_mask = build_large_mark_mask(gray, text_mask)

    text_ratio = np.count_nonzero(text_mask) / area
    ink_ratio = np.count_nonzero(ink_mask) / area
    edge_ratio = np.count_nonzero(edge_mask) / area
    handwriting_ratio = np.count_nonzero(handwriting_mask > 24) / area
    large_mark_ratio = np.count_nonzero(large_mark_mask > 0) / area
    graphic_ratio = max(0.0, edge_ratio - text_ratio * 0.18)

    return {
        "text_ratio": text_ratio,
        "ink_ratio": ink_ratio,
        "edge_ratio": edge_ratio,
        "handwriting_ratio": handwriting_ratio,
        "large_mark_ratio": large_mark_ratio,
        "graphic_ratio": graphic_ratio,
    }


def resolve_document_mode(requested_mode: str, profile: dict[str, float]) -> str:
    if requested_mode != DOCUMENT_MODE_AUTO:
        return requested_mode

    if profile["handwriting_ratio"] >= 0.014 or profile["large_mark_ratio"] >= 0.010:
        return DOCUMENT_MODE_EXAM
    if profile["graphic_ratio"] >= 0.050 and profile["text_ratio"] <= 0.18:
        return DOCUMENT_MODE_BOOK
    if profile["text_ratio"] >= 0.11:
        return DOCUMENT_MODE_EXAM
    return DOCUMENT_MODE_BOOK


def describe_document_mode(document_mode: str) -> str:
    labels = {
        DOCUMENT_MODE_AUTO: "자동",
        DOCUMENT_MODE_EXAM: "시험지 복원",
        DOCUMENT_MODE_BOOK: "교재 스캔",
    }
    return labels.get(document_mode, document_mode)


def plan_restoration(
    requested_document_mode: str,
    requested_restoration_mode: str,
    profile: dict[str, float],
) -> tuple[str, str]:
    resolved_document_mode = resolve_document_mode(requested_document_mode, profile)
    resolved_restoration_mode = requested_restoration_mode

    if requested_restoration_mode == RESTORATION_MODE_PRECISE and resolved_document_mode == DOCUMENT_MODE_BOOK:
        if profile["graphic_ratio"] >= 0.065 and profile["handwriting_ratio"] < 0.010:
            resolved_restoration_mode = RESTORATION_MODE_FAST

    return resolved_document_mode, resolved_restoration_mode


def extract_restore_candidates(original_gray: np.ndarray, cleaned_gray: np.ndarray, text_mask: np.ndarray) -> list[tuple[int, int, int, int]]:
    weakened = ((cleaned_gray.astype(np.int16) - original_gray.astype(np.int16)) > 34).astype(np.uint8) * 255
    weakened = cv2.bitwise_and(weakened, text_mask)
    weakened = cv2.dilate(weakened, np.ones((5, 5), np.uint8), iterations=1)
    weakened = cv2.morphologyEx(weakened, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8), iterations=1)

    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(weakened, 8, cv2.CV_32S)
    candidates: list[tuple[int, int, int, int]] = []
    height, width = original_gray.shape

    for idx in range(1, num_labels):
        x, y, w, h, area = stats[idx]
        if area < 120:
            continue
        if w < 30 or h < 14:
            continue
        if w > width * 0.85 or h > height * 0.25:
            continue

        pad = 10
        x0 = max(0, x - pad)
        y0 = max(0, y - pad)
        x1 = min(width, x + w + pad)
        y1 = min(height, y + h + pad)
        candidates.append((x0, y0, x1, y1))

    candidates.sort(key=lambda box: (box[3] - box[1]) * (box[2] - box[0]), reverse=True)
    return candidates[:6]


def should_restore_with_api(client: genai.Client, original_crop: np.ndarray, cleaned_crop: np.ndarray) -> bool:
    prompt = (
        "You are checking whether printed text was damaged by document cleanup. "
        "Compare the original crop and the cleaned crop. "
        "Ignore remaining handwriting or circles. "
        "Return JSON only in the form {\"restore\": true} if the cleaned crop lost or weakened printed text that should be restored. "
        "Return {\"restore\": false} if printed text is already readable enough."
    )
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[prompt, bgr_to_part(original_crop), bgr_to_part(cleaned_crop)],
        config=types.GenerateContentConfig(
            temperature=0,
            response_mime_type="application/json",
        ),
    )
    text = (response.text or "").strip()
    parsed = json.loads(text)
    return bool(parsed.get("restore", False))


def locally_restore_text(original_bgr: np.ndarray, cleaned_bgr: np.ndarray, box: tuple[int, int, int, int]) -> None:
    x0, y0, x1, y1 = box
    original_crop = original_bgr[y0:y1, x0:x1]
    cleaned_crop = cleaned_bgr[y0:y1, x0:x1]

    original_gray = cv2.cvtColor(original_crop, cv2.COLOR_BGR2GRAY)
    cleaned_gray = cv2.cvtColor(cleaned_crop, cv2.COLOR_BGR2GRAY)
    text_mask = cv2.adaptiveThreshold(
        original_gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        41,
        15,
    )
    damaged_mask = ((cleaned_gray.astype(np.int16) - original_gray.astype(np.int16)) > 28).astype(np.uint8) * 255
    restore_mask = cv2.bitwise_and(text_mask, damaged_mask)
    restore_mask = cv2.dilate(restore_mask, np.ones((2, 2), np.uint8), iterations=1)

    if not np.any(restore_mask):
        return

    cleaned_f = cleaned_crop.astype(np.float32)
    original_f = original_crop.astype(np.float32)
    alpha = (cv2.GaussianBlur(restore_mask, (0, 0), 1.2).astype(np.float32) / 255.0)[..., None]
    blended = cleaned_f * (1.0 - alpha) + original_f * alpha
    cleaned_bgr[y0:y1, x0:x1] = np.clip(blended, 0, 255).astype(np.uint8)


def rescue_text_regions(
    original_bgr: np.ndarray,
    cleaned_bgr: np.ndarray,
    text_mask: np.ndarray,
    api_rescue: str,
    api_key: str | None,
) -> np.ndarray:
    if api_rescue == API_RESCUE_OFF:
        return cleaned_bgr

    original_gray = cv2.cvtColor(original_bgr, cv2.COLOR_BGR2GRAY)
    cleaned_gray = cv2.cvtColor(cleaned_bgr, cv2.COLOR_BGR2GRAY)
    candidates = extract_restore_candidates(original_gray, cleaned_gray, text_mask)
    if not candidates:
        return cleaned_bgr

    client = None
    if api_rescue in {API_RESCUE_AUTO, API_RESCUE_ON} and api_key:
        client = genai.Client(api_key=api_key)
    elif api_rescue == API_RESCUE_ON and not api_key:
        log("4/5", "API 복원이 켜져 있지만 GOOGLE_API_KEY가 없어 로컬 복원만 적용합니다.")

    for index, box in enumerate(candidates, start=1):
        x0, y0, x1, y1 = box
        do_restore = True
        if client is not None:
            try:
                do_restore = should_restore_with_api(client, original_bgr[y0:y1, x0:x1], cleaned_bgr[y0:y1, x0:x1])
                log("4/5", f"복원 후보 {index}/{len(candidates)} API 판정: {'복원' if do_restore else '건너뜀'}")
            except Exception as exc:
                log("4/5", f"API 복원 판정 실패, 로컬 기준으로 진행합니다: {exc}")
                do_restore = True

        if do_restore:
            locally_restore_text(original_bgr, cleaned_bgr, box)

    if client is not None:
        client.close()
    return cleaned_bgr


def soften_handwriting(gray: np.ndarray, text_mask: np.ndarray, strength: float) -> np.ndarray:
    mark_mask = build_handwriting_mask(gray, text_mask)
    if not np.any(mark_mask):
        return gray

    blur_mask = mark_mask.astype(np.float32) / 255.0
    gray_f = gray.astype(np.float32)
    lifted = gray_f + (255.0 - gray_f) * blur_mask * strength
    lifted = cv2.GaussianBlur(lifted.astype(np.uint8), (0, 0), 0.6).astype(np.float32)
    return np.clip(lifted, 0, 255).astype(np.uint8)


def enhance_color_document(
    image: np.ndarray,
    cleaned_gray: np.ndarray,
    luminance_mix: float = 0.28,
    background_boost_strength: float = 0.28,
) -> np.ndarray:
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l_channel, a_channel, b_channel = cv2.split(lab)

    mixed_l = cv2.addWeighted(l_channel, 1.0 - luminance_mix, cleaned_gray, luminance_mix, 0)
    merged = cv2.merge((mixed_l, a_channel, b_channel))
    color = cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)

    base_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY).astype(np.float32)
    cleaned_f = cleaned_gray.astype(np.float32)
    improvement = np.clip((cleaned_f - base_gray) / 255.0, 0.0, 1.0)
    improvement = cv2.GaussianBlur(improvement, (0, 0), 3)

    background_mask = np.clip((cleaned_f - 168.0) / 72.0, 0.0, 1.0)
    boost = improvement * background_mask * background_boost_strength

    color_f = color.astype(np.float32)
    color_f = color_f + (255.0 - color_f) * boost[..., None]
    return np.clip(color_f, 0, 255).astype(np.uint8)


def render_style(
    image: np.ndarray,
    style: str,
    handwriting: str,
    document_mode: str,
    restoration_mode: str,
    api_rescue: str,
    api_key: str | None,
) -> tuple[np.ndarray, str, str, dict[str, float]]:
    original_bgr = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    probe_normalized = normalize_gray(gray)
    _, probe_text_mask = protect_text_denoise(probe_normalized)
    profile = analyze_page_profile(probe_normalized, probe_text_mask)
    resolved_mode, resolved_restoration_mode = plan_restoration(document_mode, restoration_mode, profile)

    if resolved_mode == DOCUMENT_MODE_EXAM:
        clip_limit = 3.1
        denoise_strength = 19
        soften_bonus = 0.10
        background_boost = 0.32
        luminance_mix = 0.31
        bw_suppression = 0.98
        scan_beta = 12
    else:
        clip_limit = 2.3
        denoise_strength = 15
        soften_bonus = -0.12
        background_boost = 0.16
        luminance_mix = 0.18
        bw_suppression = 0.78
        scan_beta = 7

    if resolved_restoration_mode == RESTORATION_MODE_PRECISE:
        clip_limit += 0.25
        denoise_strength += 1
        soften_bonus += 0.08 if resolved_mode == DOCUMENT_MODE_EXAM else -0.04
        background_boost += 0.05 if resolved_mode == DOCUMENT_MODE_EXAM else 0.02
        luminance_mix += 0.03 if resolved_mode == DOCUMENT_MODE_EXAM else 0.02
        bw_suppression = min(1.0, bw_suppression + 0.05)
        scan_beta += 2

    normalized = normalize_gray(gray, clip_limit=clip_limit)
    cleaned_gray, text_mask = protect_text_denoise(normalized, denoise_strength=denoise_strength)

    if handwriting == HANDWRITING_SOFTEN:
        soften_strength = 0.55 if style == STYLE_COLOR else 0.88
        soften_strength = min(0.98, max(0.18, soften_strength + soften_bonus))
        cleaned_gray = soften_handwriting(cleaned_gray, text_mask, strength=soften_strength)

    if style == STYLE_BW:
        if handwriting == HANDWRITING_SOFTEN:
            cleaned_gray = suppress_marks_for_bw(cleaned_gray, text_mask, strength=bw_suppression)
        threshold = cv2.adaptiveThreshold(
            cleaned_gray,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            35,
            13,
        )
        threshold = cv2.medianBlur(threshold, 3)
        result = cv2.cvtColor(threshold, cv2.COLOR_GRAY2BGR)
        return (
            rescue_text_regions(original_bgr, result, text_mask, api_rescue, api_key),
            resolved_mode,
            resolved_restoration_mode,
            profile,
        )

    if style == STYLE_SCAN:
        boosted = cv2.convertScaleAbs(cleaned_gray, alpha=1.08, beta=scan_beta)
        scan = cv2.adaptiveThreshold(
            boosted,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            45,
            11,
        )
        scan = cv2.medianBlur(scan, 3)
        result = cv2.cvtColor(scan, cv2.COLOR_GRAY2BGR)
        return (
            rescue_text_regions(original_bgr, result, text_mask, api_rescue, api_key),
            resolved_mode,
            resolved_restoration_mode,
            profile,
        )

    result = enhance_color_document(
        image,
        cleaned_gray,
        luminance_mix=luminance_mix,
        background_boost_strength=background_boost,
    )
    return (
        rescue_text_regions(original_bgr, result, text_mask, api_rescue, api_key),
        resolved_mode,
        resolved_restoration_mode,
        profile,
    )


def clean_page(
    image: np.ndarray,
    style: str,
    handwriting: str,
    document_mode: str,
    restoration_mode: str,
    api_rescue: str,
    api_key: str | None,
) -> np.ndarray:
    corners = detect_document(image)
    if corners is not None:
        log("2/5", "문서 영역을 찾았습니다. 원근 보정을 적용합니다.")
        image = four_point_transform(image, corners)
    else:
        log("2/5", "문서 외곽을 확실히 찾지 못해 전체 이미지를 기준으로 진행합니다.")

    log("3/5", "배경 정리와 밝기 보정을 적용합니다.")
    result, resolved_mode, resolved_restoration_mode, profile = render_style(
        image,
        style=style,
        handwriting=handwriting,
        document_mode=document_mode,
        restoration_mode=restoration_mode,
        api_rescue=api_rescue,
        api_key=api_key,
    )
    log(
        "3/5",
        (
            f"문서 모드: {describe_document_mode(resolved_mode)} | 복원 방식: {describe_restoration_mode(resolved_restoration_mode)} "
            f"(text={profile['text_ratio']:.3f}, marks={profile['handwriting_ratio']:.3f}, graphics={profile['graphic_ratio']:.3f})"
        ),
    )
    return result


def ensure_output_path(input_path: Path, output_path: str | None, suffix: str) -> Path:
    if output_path:
        return Path(output_path)
    output_dir = Path(__file__).resolve().parent / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir / f"{input_path.stem}_cleaned{suffix}"


def load_pages(input_path: Path, dpi: int) -> list[Image.Image]:
    if input_path.suffix.lower() == ".pdf":
        pages = convert_from_path(str(input_path), dpi=dpi)
        return pages
    return [Image.open(input_path).convert("RGB")]


def save_results(results: list[np.ndarray], output_path: Path) -> None:
    if output_path.suffix.lower() == ".pdf":
        pil_pages = [bgr_to_pil(page).convert("RGB") for page in results]
        pil_pages[0].save(
            str(output_path),
            save_all=True,
            append_images=pil_pages[1:],
        )
        return

    if len(results) == 1:
        bgr_to_pil(results[0]).save(output_path)
        return

    output_path.mkdir(parents=True, exist_ok=True)
    for index, page in enumerate(results, start=1):
        page_path = output_path / f"page_{index:03d}.png"
        bgr_to_pil(page).save(page_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="문서 스캔 정리기")
    parser.add_argument("input", help="입력 파일 경로(PDF 또는 이미지)")
    parser.add_argument("--output", help="출력 파일 또는 폴더 경로")
    parser.add_argument(
        "--document-mode",
        choices=[DOCUMENT_MODE_AUTO, DOCUMENT_MODE_EXAM, DOCUMENT_MODE_BOOK],
        default=DOCUMENT_MODE_AUTO,
    )
    parser.add_argument(
        "--restoration-mode",
        choices=[RESTORATION_MODE_FAST, RESTORATION_MODE_PRECISE],
        default=RESTORATION_MODE_FAST,
    )
    parser.add_argument("--style", choices=[STYLE_COLOR, STYLE_SCAN, STYLE_BW], default=STYLE_COLOR)
    parser.add_argument("--handwriting", choices=[HANDWRITING_KEEP, HANDWRITING_SOFTEN], default=HANDWRITING_KEEP)
    parser.add_argument("--api-rescue", choices=[API_RESCUE_OFF, API_RESCUE_AUTO, API_RESCUE_ON], default=API_RESCUE_AUTO)
    parser.add_argument("--dpi", type=int, default=200)
    args = parser.parse_args()

    started = time.time()
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"오류: 입력 파일을 찾을 수 없습니다 -> {input_path}")
        sys.exit(1)

    suffix = ".pdf" if input_path.suffix.lower() == ".pdf" else ".png"
    output_path = ensure_output_path(input_path, args.output, suffix)
    api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")

    log("1/5", f"입력 파일을 불러옵니다: {input_path.name}")
    pages = load_pages(input_path, dpi=args.dpi)
    log("1/5", f"총 {len(pages)}페이지를 준비했습니다.")

    results = []
    for page_index, page in enumerate(pages, start=1):
        log("2/5", f"페이지 {page_index}/{len(pages)} 처리 시작")
        bgr = pil_to_bgr(page)
        cleaned = clean_page(
            bgr,
            style=args.style,
            handwriting=args.handwriting,
            document_mode=args.document_mode,
            restoration_mode=args.restoration_mode,
            api_rescue=args.api_rescue,
            api_key=api_key,
        )
        results.append(cleaned)
        log("4/5", f"페이지 {page_index}/{len(pages)} 정리 완료")

    log("5/5", "결과 파일을 저장합니다.")
    save_results(results, output_path)
    log("5/5", f"저장 완료: {output_path}")
    log("5/5", f"총 소요 시간: {int(time.time() - started)}초")


if __name__ == "__main__":
    main()
