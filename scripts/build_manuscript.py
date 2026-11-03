#!/usr/bin/env python3
"""Combine numbered manuscript Markdown files into output/manuscript.md."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
parts = sorted((ROOT / "manuscript").glob("[0-9][0-9]-*.md"))
if len(parts) != 15 or parts[0].name != "00-title.md" or parts[-1].name != "14-references.md":
    raise SystemExit("Expected 15 ordered sections (00-title.md through 14-references.md)")
output = ROOT / "output" / "manuscript.md"
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text("\n\n".join(p.read_text(encoding="utf-8").rstrip() for p in parts) + "\n", encoding="utf-8")
print(f"Wrote {output} ({len(parts)} sections)")
