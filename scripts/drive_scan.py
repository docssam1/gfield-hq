#!/usr/bin/env python3
import csv
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
ROOT_FOLDER_ID = os.environ.get("GFIELD_DRIVE_ROOT_FOLDER_ID", "").strip()
OUTPUT_DIR = Path(os.environ.get("GFIELD_OUTPUT_DIR", "/home/gfield7265/gfield_output/drive_inventory"))


def classify_file(name: str, mime_type: str) -> str:
    text = f"{name} {mime_type}".lower()
    if any(k in text for k in ["report", "리포트", "학습", "상담"]):
        return "report_or_consultation"
    if any(k in text for k in ["홈페이지", "homepage", "html", "랜딩", "landing"]):
        return "homepage_asset"
    if any(k in text for k in ["교재", "문제", "worksheet", "pdf", "황소", "소마", "필즈"]):
        return "teaching_material"
    if any(k in text for k in ["kakao", "카카오", "talk"]):
        return "kakao_export"
    if any(k in text for k in ["video", "youtube", "mp4", "영상"]):
        return "video"
    if mime_type.startswith("image/") or any(k in text for k in ["jpg", "jpeg", "png", "photo", "사진"]):
        return "image_or_photo"
    return "unknown"


def get_drive_service():
    cred_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "").strip()
    if not cred_path or not Path(cred_path).exists():
        raise RuntimeError("GOOGLE_APPLICATION_CREDENTIALS is missing or file does not exist")
    creds = service_account.Credentials.from_service_account_file(cred_path, scopes=SCOPES)
    return build("drive", "v3", credentials=creds)


def list_files(service):
    query = "trashed=false"
    if ROOT_FOLDER_ID:
        query = f"'{ROOT_FOLDER_ID}' in parents and trashed=false"

    fields = "nextPageToken, files(id,name,mimeType,parents,webViewLink,createdTime,modifiedTime,size)"
    page_token = None
    rows = []
    while True:
        resp = service.files().list(
            q=query,
            spaces="drive",
            fields=fields,
            pageToken=page_token,
            pageSize=1000,
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
                "parents": ",".join(f.get("parents", [])),
            })
        page_token = resp.get("nextPageToken")
        if not page_token:
            break
    return rows


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    service = get_drive_service()
    rows = list_files(service)
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    csv_path = OUTPUT_DIR / f"drive_inventory_{ts}.csv"
    json_path = OUTPUT_DIR / f"drive_inventory_{ts}.json"
    summary_path = OUTPUT_DIR / "latest_summary.txt"

    fieldnames = ["id", "name", "mimeType", "category", "createdTime", "modifiedTime", "size", "webViewLink", "parents"]
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    json_path.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")

    counts = {}
    for r in rows:
        counts[r["category"]] = counts.get(r["category"], 0) + 1
    lines = [
        "GFIELD Drive Scan Summary",
        f"time_utc: {ts}",
        f"root_folder_id: {ROOT_FOLDER_ID or 'ALL_ACCESSIBLE_FILES'}",
        f"total_files: {len(rows)}",
        "category_counts:",
    ]
    for k in sorted(counts):
        lines.append(f"- {k}: {counts[k]}")
    lines.append(f"csv: {csv_path}")
    lines.append(f"json: {json_path}")
    summary_path.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
