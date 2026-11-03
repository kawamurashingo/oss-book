#!/usr/bin/env python3
"""Report unresolved publication metadata without blocking draft previews.

Use --enforce to fail before preparing a final publication. This only checks
metadata completeness, NOT copyright clearance or event-specific requirements.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMPRINT = ROOT / "publication" / "imprint.json"
REQUIRED = {
    "author": "著者名",
    "publisher": "発行者・サークル名",
    "publication_date": "発行日",
    "copyright": "著作権表示",
}
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
    return unresolved


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--enforce", action="store_true",
        help="return nonzero if mandatory imprint fields are incomplete",
    )
    args = parser.parse_args()
    try:
        data = json.loads(IMPRINT.read_text(encoding="utf-8"))
        unresolved = unresolved_fields(data)
    except (ValueError, OSError) as exc:
        parser.exit(2, f"Invalid publication metadata: {exc}\n")
    if unresolved:
        print("DRAFT ONLY — 奥付の未確定項目：")
        for field in unresolved:
            print(f"  - {field}")
        print("発行前の権利確認・読者校正・技術書典の登録条件も別途必要です。")
        return 1 if args.enforce else 0
    print("奥付の必須項目は入力済み（出版準備全体の完了を意味しません）。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
