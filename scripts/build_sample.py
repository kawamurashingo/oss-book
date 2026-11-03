#!/usr/bin/env python3
"""Build a promotional *excerpt* PDF from the same manuscript as the full book.

Requires output/cover.png: run scripts/build_release.py first.
This is a reader-facing teaser, NOT the full review copy required by a publisher.
"""
from __future__ import annotations

import html
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output"
SAMPLE_FILENAMES = (
    "01-introduction.md",
    "02-prologue.md",
    "03-chapter-01.md",
    "04-chapter-02.md",
)


def sample_markdown() -> str:
    """Read *whole* sections, in their original order, without rewriting text."""
    manuscript = ROOT / "manuscript"
    parts = []
    for name in SAMPLE_FILENAMES:
        path = manuscript / name
        if not path.is_file():
            raise FileNotFoundError(f"Sample chapter is missing: {path}")
        content = path.read_text(encoding="utf-8").rstrip()
        if not content.startswith("# "):
            raise ValueError(f"Not a complete chapter: {path}")
        parts.append(content)
    return "\n\n".join(parts) + "\n"


def book_title() -> str:
    metadata = (ROOT / "book.yaml").read_text(encoding="utf-8")
    match = re.search(r"^title:\s*(.+)$", metadata, flags=re.MULTILINE)
    if not match:
        raise ValueError("Missing book title")
    return match.group(1).strip().strip('"')


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    cover_image = OUT / "cover.png"
    if not cover_image.is_file():
        raise SystemExit("First run: python3 scripts/build_release.py (generates cover.png)")

    from weasyprint import CSS, HTML

    source = OUT / "sample-body.md"
    source.write_text(sample_markdown(), encoding="utf-8")
    html_file = OUT / "oss-book-sample.html"
    pdf_file = OUT / "oss-book-sample.pdf"

    from json import loads
    imprint = loads((ROOT / "publication" / "imprint.json").read_text(encoding="utf-8"))
    cmd = [
        "pandoc", str(source), "--from=markdown", "--standalone",
        "--table-of-contents", "--toc-depth=1", "--metadata-file=book.yaml",
    ]
    author = imprint.get("author", "")
    if author:
        cmd.extend(["--metadata", f"author={author}"])
    subprocess.run([*cmd, "--to=html5", "--output", str(html_file)], cwd=ROOT, check=True)
    page = html_file.read_text(encoding="utf-8")
    if "<body>" not in page or 'id="TOC"' not in page:
        raise SystemExit("Pandoc did not generate the expected body and TOC")
    cover_uri = html.escape(cover_image.resolve().as_uri(), quote=True)
    title = html.escape(book_title(), quote=True)
    fragment = (
        '<section class="book-cover">'
        f'<img src="{cover_uri}" alt="{title} 表紙"/>'
        '<span class="sample-stamp">試し読み</span>'
        '</section>'
    )
    html_file.write_text(page.replace("<body>", "<body>\n" + fragment + "\n", 1), encoding="utf-8")
    HTML(filename=html_file, base_url=ROOT).write_pdf(pdf_file, stylesheets=[
        CSS(filename=ROOT / "styles" / "book.css"),
        CSS(filename=ROOT / "styles" / "sample.css"),
    ])
    print(f"Sample PDF: {pdf_file} ({pdf_file.stat().st_size:,} bytes)")
    print("Sample sections:", ", ".join(SAMPLE_FILENAMES))


if __name__ == "__main__":
    main()
