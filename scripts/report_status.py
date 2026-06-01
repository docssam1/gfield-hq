#!/usr/bin/env python3
import json
from pathlib import Path

KAKAO_DIR = Path("/home/gfield7265/gfield_output/kakao_inventory")
REPORT_DIR = Path("/home/gfield7265/gfield_output/report_inventory")


def latest_file(path: Path, prefix: str) -> Path | None:
    files = sorted(path.glob(f"{prefix}_*.json"), key=lambda p: p.stat().st_mtime)
    return files[-1] if files else None


def count_rows(json_path: Path | None) -> int:
    if not json_path:
        return 0
    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
        return len(data) if isinstance(data, list) else 0
    except Exception:
        return 0


def main() -> None:
    kakao_latest = latest_file(KAKAO_DIR, "kakao_inventory")
    report_latest = latest_file(REPORT_DIR, "report_inventory")

    print("GFIELD Report Status")
    if kakao_latest:
        print(f"kakao_latest: {kakao_latest}")
        print(f"kakao_count: {count_rows(kakao_latest)}")
    else:
        print("kakao_latest: none")

    if report_latest:
        print(f"report_latest: {report_latest}")
        print(f"report_count: {count_rows(report_latest)}")
    else:
        print("report_latest: none")


if __name__ == "__main__":
    main()

