#!/usr/bin/env python3
import csv
import json
import re
from datetime import datetime, timezone
from pathlib import Path

INPUT_DIR = Path("/home/gfield7265/gfield_output/drive_inventory")
OUTPUT_DIR = Path("/home/gfield7265/gfield_output/kakao_inventory")

KAKAO_KEYWORDS = [
    "kakao", "카카오", "talk", "톡", "채팅", "대화", "상담",
]
REPORT_HINT_KEYWORDS = [
    "리포트", "report", "학습", "과제", "숙제", "피드백", "오답", "진도", "수업",
]


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip()).lower()


def score_text(text: str, keywords: list[str]) -> int:
    t = normalize(text)
    return sum(1 for k in keywords if k.lower() in t)


def latest_inventory_json() -> Path:
    files = sorted(INPUT_DIR.glob("drive_inventory_*.json"), key=lambda p: p.stat().st_mtime)
    if not files:
        raise FileNotFoundError(f"No inventory json found in {INPUT_DIR}")
    return files[-1]


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    src = latest_inventory_json()
    rows = json.loads(src.read_text(encoding="utf-8"))
    if not isinstance(rows, list):
        raise ValueError(f"Inventory format invalid: {src}")

    picked = []
    for r in rows:
        name = str(r.get("name", ""))
        mime_type = str(r.get("mimeType", ""))
        category = str(r.get("category", ""))
        base_text = f"{name} {mime_type} {category}"

        kakao_score = score_text(base_text, KAKAO_KEYWORDS)
        if kakao_score == 0 and category != "kakao":
            continue

        report_hint_score = score_text(base_text, REPORT_HINT_KEYWORDS)
        picked.append(
            {
                "id": r.get("id", ""),
                "name": name,
                "mimeType": mime_type,
                "category": category,
                "kakao_score": kakao_score,
                "report_hint_score": report_hint_score,
                "createdTime": r.get("createdTime", ""),
                "modifiedTime": r.get("modifiedTime", ""),
                "size": r.get("size", ""),
                "webViewLink": r.get("webViewLink", ""),
            }
        )

    picked.sort(key=lambda x: (x["kakao_score"], x["report_hint_score"], x.get("modifiedTime", "")), reverse=True)

    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    out_json = OUTPUT_DIR / f"kakao_inventory_{ts}.json"
    out_csv = OUTPUT_DIR / f"kakao_inventory_{ts}.csv"

    out_json.write_text(json.dumps(picked, ensure_ascii=False, indent=2), encoding="utf-8")

    fields = [
        "id", "name", "mimeType", "category", "kakao_score", "report_hint_score",
        "createdTime", "modifiedTime", "size", "webViewLink",
    ]
    with out_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(picked)

    print("GFIELD Kakao Inventory Summary")
    print(f"source: {src}")
    print(f"total_candidates: {len(picked)}")
    print(f"json: {out_json}")
    print(f"csv: {out_csv}")
    print("top_samples: 20")
    for i, row in enumerate(picked[:20], start=1):
        print(
            f"{i:02d}. "
            f"kakao={row['kakao_score']} report_hint={row['report_hint_score']} | "
            f"{row['name']}"
        )


if __name__ == "__main__":
    main()

