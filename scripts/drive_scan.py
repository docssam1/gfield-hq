#!/usr/bin/env python3
import csv
import json
from datetime import datetime, timezone
from pathlib import Path

import google.auth
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
OUTPUT_DIR = Path("/home/gfield7265/gfield_output/drive_inventory")


def get_drive_service():
    creds, _ = google.auth.default(scopes=SCOPES)
    return build("drive", "v3", credentials=creds)


def classify_file(name, mime_type):
    text = f"{name} {mime_type}".lower()
    if any(k in text for k in ["리포트", "report", "상담", "학습보고", "학습 보고"]):
        return "report"
    if any(k in text for k in ["홈페이지", "homepage", "landing", "랜딩", "html", "web", "사이트"]):
        return "homepage"
    if any(k in text for k in ["교재", "문제", "문항", "worksheet", "pdf", "황소", "소마", "필즈", "초등", "수학", "모의고사", "기출", "유사", "해설", "풀이", "단평", "퀵테"]):
        return "material"
    if any(k in text for k in ["카카오", "kakao", "talk", "채팅", "대화"]):
        return "kakao"
    if any(k in text for k in ["영상", "video", "mp4", "mov", "youtube", "강의"]):
        return "video"
    if mime_type.startswith("image/") or any(k in text for k in ["jpg", "jpeg", "png", "사진", "photo", "screenshot", "스크린샷"]):
        return "image"
    if "spreadsheet" in mime_type or any(k in text for k in ["xlsx", "xls", "sheet", "시트", "명단", "수납", "출결"]):
        return "sheet_or_db"
    if "presentation" in mime_type or any(k in text for k in ["ppt", "slides", "발표", "설명회"]):
        return "presentation"
    if "document" in mime_type or any(k in text for k in ["docx", "문서", "공지", "안내"]):
        return "document"
    return "unknown"


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    service = get_drive_service()
    rows, page_token = [], None

    while True:
        resp = service.files().list(
            q="trashed=false",
            spaces="drive",
            pageSize=1000,
            pageToken=page_token,
            fields="nextPageToken, files(id,name,mimeType,createdTime,modifiedTime,size,webViewLink)",
            supportsAllDrives=True,
            includeItemsFromAllDrives=True,
        ).execute()

        for f in resp.get("files", []):
            rows.append({
                "id": f.get("id", ""),
                "name": f.get("name", ""),
                "mimeType": f.get("mimeType", ""),
                "category": classify_file(f.get("name", ""), f.get("mimeType", "")),
                "createdTime": f.get("createdTime", ""),
                "modifiedTime": f.get("modifiedTime", ""),
                "size": f.get("size", ""),
                "webViewLink": f.get("webViewLink", ""),
            })

        page_token = resp.get("nextPageToken")
        if not page_token:
            break

    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    csv_path = OUTPUT_DIR / f"drive_inventory_{ts}.csv"
    json_path = OUTPUT_DIR / f"drive_inventory_{ts}.json"
    unknown_path = OUTPUT_DIR / f"unknown_sample_{ts}.txt"

    fields = ["id", "name", "mimeType", "category", "createdTime", "modifiedTime", "size", "webViewLink"]
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    json_path.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")

    counts = {}
    unknown_names = []
    for r in rows:
        counts[r["category"]] = counts.get(r["category"], 0) + 1
        if r["category"] == "unknown" and len(unknown_names) < 80:
            unknown_names.append(r["name"])
    unknown_path.write_text("\n".join(unknown_names), encoding="utf-8")

    print("GFIELD Drive Scan Summary")
    print(f"total_files: {len(rows)}")
    for k, v in sorted(counts.items()):
        print(f"- {k}: {v}")
    print(f"csv: {csv_path}")
    print(f"json: {json_path}")
    print(f"unknown_sample: {unknown_path}")


if __name__ == "__main__":
    main()
