#!/usr/bin/env python3
import csv
import json
import re
from datetime import datetime, timezone
from pathlib import Path

INPUT_DIR = Path("/home/gfield7265/gfield_output/drive_inventory")
OUTPUT_DIR = Path("/home/gfield7265/gfield_output/report_inventory")

REPORT_KEYWORDS = [
    "report", "리포트", "학습", "과제", "숙제", "피드백", "오답", "진도", "수업", "상담",
]
MATERIAL_KEYWORDS = [
    "worksheet", "교재", "문항", "문제", "pdf", "모의고사", "기출", "해설",
]
KAKAO_KEYWORDS = [
    "kakao", "카카오", "talk", "채팅", "대화", "상담",
]
TYPE_HINTS = {
    "report": ["report", "리포트", "학습보고", "피드백"],
    "kakao": ["kakao", "카카오", "talk", "채팅", "대화", "상담"],
    "material": ["worksheet", "교재", "문제", "문항", "pdf", "모의고사", "기출", "해설"],
    "video": ["video", "영상", "강의", "mp4", "mov", "youtube"],
    "sheet_or_db": ["sheet", "xlsx", "xls", "시트", "출결", "명단"],
}


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip()).lower()


def latest_inventory_json() -> Path:
    files = sorted(INPUT_DIR.glob("drive_inventory_*.json"), key=lambda p: p.stat().st_mtime)
    if not files:
        raise FileNotFoundError(f"No inventory json found in {INPUT_DIR}")
    return files[-1]


def score(text: str, keywords: list[str]) -> int:
    t = normalize(text)
    return sum(1 for k in keywords if k.lower() in t)


def infer_type(text: str, category: str) -> str:
    t = normalize(text)
    if category in TYPE_HINTS:
        return category
    for label, keys in TYPE_HINTS.items():
        if any(k.lower() in t for k in keys):
            return label
    return "unknown"


def extract_student_candidate(name: str) -> str:
    n = normalize(name)
    # Conservative: keep only simple Hangul/English 2~4 chars as candidate token groups
    tokens = re.findall(r"[가-힣]{2,4}|[a-z]{2,12}", n)
    blocked = {"report", "kakao", "talk", "sheet", "pdf", "homework", "class", "수업", "학습", "리포트"}
    for tok in tokens:
        if tok not in blocked:
            return tok
    return ""


def extract_date_candidate(name: str, created: str, modified: str) -> str:
    n = name or ""
    m = re.search(r"(20\d{2}[._-]?\d{2}[._-]?\d{2})", n)
    if m:
        raw = m.group(1)
        return raw.replace(".", "-").replace("_", "-")
    for t in [modified, created]:
        if t:
            return t[:10]
    return ""


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    src = latest_inventory_json()
    rows = json.loads(src.read_text(encoding="utf-8"))
    if not isinstance(rows, list):
        raise ValueError(f"Inventory format invalid: {src}")

    candidates = []
    for r in rows:
        name = str(r.get("name", ""))
        mime_type = str(r.get("mimeType", ""))
        category = str(r.get("category", ""))
        base = f"{name} {mime_type} {category}"
        s_report = score(base, REPORT_KEYWORDS)
        s_material = score(base, MATERIAL_KEYWORDS)
        s_kakao = score(base, KAKAO_KEYWORDS)

        if category in {"report", "material", "kakao"} or (s_report + s_material + s_kakao) > 0:
            inferred_type = infer_type(base, category)
            candidates.append(
                {
                    "id": r.get("id", ""),
                    "name": name,
                    "mimeType": mime_type,
                    "category": category,
                    "inferred_type": inferred_type,
                    "report_score": s_report,
                    "material_score": s_material,
                    "kakao_score": s_kakao,
                    "student_candidate": extract_student_candidate(name),
                    "date_candidate": extract_date_candidate(
                        name,
                        str(r.get("createdTime", "")),
                        str(r.get("modifiedTime", "")),
                    ),
                    "createdTime": r.get("createdTime", ""),
                    "modifiedTime": r.get("modifiedTime", ""),
                    "size": r.get("size", ""),
                    "webViewLink": r.get("webViewLink", ""),
                }
            )

    candidates.sort(
        key=lambda x: (x["report_score"], x["material_score"], x["kakao_score"], x.get("modifiedTime", "")),
        reverse=True,
    )

    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    out_json = OUTPUT_DIR / f"report_inventory_{ts}.json"
    out_csv = OUTPUT_DIR / f"report_inventory_{ts}.csv"

    out_json.write_text(json.dumps(candidates, ensure_ascii=False, indent=2), encoding="utf-8")
    fields = [
        "id", "name", "mimeType", "category", "inferred_type",
        "report_score", "material_score", "kakao_score",
        "student_candidate", "date_candidate",
        "createdTime", "modifiedTime", "size", "webViewLink",
    ]
    with out_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(candidates)

    print("GFIELD Report Inventory Summary")
    print(f"source: {src}")
    print(f"total_candidates: {len(candidates)}")
    print(f"json: {out_json}")
    print(f"csv: {out_csv}")
    print("top_samples: 20")
    for i, row in enumerate(candidates[:20], start=1):
        print(
            f"{i:02d}. type={row['inferred_type']} report={row['report_score']} "
            f"mat={row['material_score']} kakao={row['kakao_score']} | {row['name']}"
        )


if __name__ == "__main__":
    main()

