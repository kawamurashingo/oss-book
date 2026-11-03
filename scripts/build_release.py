#!/usr/bin/env python3
"""Build a Japanese A5 PDF and EPUB3 from the numbered manuscript files.

Requirements: Pandoc, WeasyPrint, Noto CJK fonts.
Run: python3 scripts/build_release.py
"""
from __future__ import annotations

import html as html_lib
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output"


def run(*argv: str) -> None:
    print("+", " ".join(str(x) for x in argv), flush=True)
    subprocess.run(list(argv), cwd=ROOT, check=True)


def book_meta() -> tuple[str, str]:
    text = (ROOT / "book.yaml").read_text(encoding="utf-8")
    def field(name: str) -> str:
        match = re.search(rf"^{name}:\s*(.+)$", text, flags=re.MULTILINE)
        if not match:
            raise SystemExit(f"Missing {name} from book.yaml")
        return match.group(1).strip().strip('"\'')
    return field("title"), field("subtitle")


def main() -> None:
    run(sys.executable, "scripts/build_manuscript.py")
    OUT.mkdir(parents=True, exist_ok=True)
    parts = sorted((ROOT / "manuscript").glob("[0-9][0-9]-*.md"))
    if len(parts) != 15 or parts[0].name != "00-title.md" or parts[-1].name != "14-references.md":
        raise SystemExit("Expected 15 ordered sections including 14-references.md")

    # The first section is the editorial title leaf. Pandoc builds the actual
    # title-page and EPUB metadata from book.yaml, so exclude this leaf.
    body = OUT / "body.md"
    body.write_text(
        "\n\n".join(p.read_text(encoding="utf-8").rstrip() for p in parts[1:]) + "\n",
        encoding="utf-8",
    )
    title, subtitle = book_meta()
    html_file = OUT / "oss-book.html"
    pdf = OUT / "oss-book.pdf"
    epub = OUT / "oss-book.epub"

    common = ["pandoc", str(body), "--from=markdown", "--standalone",
              "--table-of-contents", "--toc-depth=1", "--metadata-file=book.yaml"]
    run(*common, "--to=html5", "--output", str(html_file))

    # Place a dedicated cover before the table of contents; omit Pandoc's
    # automatic HTML title header (we keep its EPUB title metadata).
    cover = (f'<section class="book-cover">'
             f'<h1>{html_lib.escape(title)}</h1>'
             f'<p class="subtitle">{html_lib.escape(subtitle)}</p>'
             f'<p class="draft-note">執筆用プレビュー（未校正）</p>'
             f'</section>')
    html_text = html_file.read_text(encoding="utf-8")
    if "<body>" not in html_text or 'id="TOC"' not in html_text:
        raise SystemExit("Unexpected Pandoc HTML structure: title/TOC absent")
    html_text = html_text.replace("<body>", "<body>\n" + cover + "\n", 1)
    html_file.write_text(html_text, encoding="utf-8")

    run(*common, "--to=epub3", "--split-level=1",
        "--css=styles/epub.css", "--output", str(epub))
    try:
        from weasyprint import CSS, HTML
    except ImportError as exc:
        raise SystemExit("Install WeasyPrint: python3 -m pip install weasyprint") from exc
    print("+ WeasyPrint ->", pdf, flush=True)
    HTML(filename=html_file, base_url=ROOT).write_pdf(
        pdf, stylesheets=[CSS(filename=ROOT / "styles/book.css")]
    )
    print(f"Generated: {pdf} ({pdf.stat().st_size:,} bytes)")
    print(f"Generated: {epub} ({epub.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
