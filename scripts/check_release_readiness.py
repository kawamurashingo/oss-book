#!/usr/bin/env python3
"""Report unresolved publication metadata without blocking draft previews.

Use --enforce to fail before preparing a final publication. This only checks
metadata completeness, NOT copyright clearance or event-specific requirements.
"""
from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMPRINT = ROOT / "publication" / "imprint.json"
REQUIRED = {
    "author": "著者名",
    "publisher": "発行者・サークル名",
    "publication_date": "発行予定日／発行日",
    "copyright": "著作権表示",
}
STATUSES = {"planned", "published"}
PLACEHOLDERS = {"tbd", "todo", "未確定", "未定", "仮", "pending"}


def unresolved_fields(data: object) -> list[str]:
    if not isinstance(data, dict):
        raise ValueError("imprint.json must be a JSON object")
    unresolved = []
    for key, label in REQUIRED.items():
        value = data.get(key, "")
        if not isinstance(value, str):
            raise ValueError(f"{key} must be a string")
        if not value.strip() or value.strip().casefold() in PLACEHOLDERS:
            unresolved.append(f"{label} ({key})")
    when = data.get("publication_date", "")
    if isinstance(when, str) and when.strip() and when.strip().casefold() not in PLACEHOLDERS:
        try:
            # ISO date makes the publication schedule unambiguous in source.
            date.fromisoformat(when.strip())
        except ValueError:
            unresolved.append("発行日（YYYY-MM-DD形式が必要） (publication_date)")
    if data.get("publication_status") not in STATUSES:
        unresolved.append("発行状態 (publication_status)")
    return unresolved


def release_blockers(data: object) -> list[str]:
    """An issue date is chosen, but publication still requires a separate action."""
    blockers = unresolved_fields(data)
    if isinstance(data, dict) and data.get("publication_status") == "planned":
        blockers.append("発行は未実施・日付は予定 (publication_status)")
    return blockers


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--enforce", action="store_true",
        help="return nonzero if mandatory imprint fields are incomplete",
    )
    args = parser.parse_args()
    try:
        data = json.loads(IMPRINT.read_text(encoding="utf-8"))
        blockers = release_blockers(data)
    except (ValueError, OSError) as exc:
        parser.exit(2, f"Invalid publication metadata: {exc}\n")
    if blockers:
        print("DRAFT ONLY — 頒布前の未完了項目：")
        for field in blockers:
            print(f"  - {field}")
        print("発行前の権利確認・読者校正・技術書典の登録条件も別途必要です。")
        return 1 if args.enforce else 0
    print("奥付の必須項目と発行状態は入力済み（出版準備全体の完了を意味しません）。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
