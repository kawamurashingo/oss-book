#!/usr/bin/env python3
"""Build a Japanese A5 PDF and EPUB3 with a shared cover and optional colophon.

Requirements: Pandoc, WeasyPrint, CairoSVG and Noto CJK fonts.
Run: python3 scripts/build_release.py
"""
from __future__ import annotations

import html as html_lib
import json
from datetime import date
import re
import subprocess
import sys
from pathlib import Path

# Use the same placeholder detection for both the preview and release audit.
# Direct invocation and package import have different Python import roots.
if __package__:
    from .check_release_readiness import unresolved_fields
else:
    from check_release_readiness import unresolved_fields

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


def imprint_metadata() -> dict[str, str]:
    p = ROOT / "publication" / "imprint.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    expected = {"author", "publisher", "publication_date", "publication_status", "copyright", "contact"}
    if not expected.issubset(data):
        raise SystemExit(f"Missing imprint keys: {sorted(expected - set(data))}")
    if any(not isinstance(data[k], str) for k in expected):
        raise SystemExit("Imprint values must be strings")
    return {k: data[k].strip() for k in expected}


def complete_imprint(data: dict[str, str]) -> bool:
    # Planned issues may have a *preview* colophon, but must say "予定".
    # Missing or invalid metadata is never printed in a book preview.
    return not unresolved_fields(data)


def make_colophon(data: dict[str, str], title: str) -> str:
    if not complete_imprint(data):
        return ""
    is_planned = data["publication_status"] == "planned"
    issue_date = date.fromisoformat(data["publication_date"])
    date_text = f"{issue_date.year}年{issue_date.month}月{issue_date.day}日"
    lines = [
        "# 奥付（発行予定・校正用）" if is_planned else "# 奥付",
        f"**{title}**",
        f"著者：{data['author']}",
        f"発行：{data['publisher']}",
        f"{'発行予定日' if is_planned else '発行日'}：{date_text}",
        f"著作権表示：{data['copyright']}",
    ]
    if data["contact"]:
        lines.append(f"連絡先：{data['contact']}")
    return "\n\n".join(lines) + "\n"


def main() -> None:
    run(sys.executable, "scripts/build_manuscript.py")
    OUT.mkdir(parents=True, exist_ok=True)
    parts = sorted((ROOT / "manuscript").glob("[0-9][0-9]-*.md"))
    if len(parts) != 15 or parts[0].name != "00-title.md" or parts[-1].name != "14-references.md":
        raise SystemExit("Expected 15 ordered sections including 14-references.md")

    title, subtitle = book_meta()
    imprint = imprint_metadata()
    has_imprint = complete_imprint(imprint)

    body = OUT / "body.md"
    body_text = "\n\n".join(p.read_text(encoding="utf-8").rstrip() for p in parts[1:]) + "\n"
    if has_imprint:
        if imprint["publication_status"] == "planned":
            print("DRAFT ONLY: preview colophon includes a planned, not actual, issue date")
        body_text += "\n\n" + make_colophon(imprint, title)
    else:
        print("Publication metadata incomplete: colophon intentionally omitted from preview")
    body.write_text(body_text, encoding="utf-8")

    from cairosvg import svg2png
    svg = (ROOT / "assets" / "cover.svg").read_text(encoding="utf-8")
    if "<!-- AUTHOR_CREDIT -->" not in svg:
        raise SystemExit("Missing AUTHOR_CREDIT marker in assets/cover.svg")
    if imprint["author"]:
        author_svg = (f'<text x="128" y="2050" font-family="Noto Sans CJK JP, sans-serif" '
                      f'font-size="40" fill="#D5DFDE">{html_lib.escape(imprint["author"])}</text>')
        svg = svg.replace("<!-- AUTHOR_CREDIT -->", author_svg)
    else:
        svg = svg.replace("<!-- AUTHOR_CREDIT -->", "")
    cover_png = OUT / "cover.png"
    svg2png(bytestring=svg.encode("utf-8"), write_to=str(cover_png), output_width=1600)

    html_file = OUT / "oss-book.html"
    pdf = OUT / "oss-book.pdf"
    epub = OUT / "oss-book.epub"
    common = [
        "pandoc", str(body), "--from=markdown", "--standalone",
        "--table-of-contents", "--toc-depth=1", "--metadata-file=book.yaml",
    ]
    if imprint["author"]:
        common.extend(["--metadata", f"author={imprint['author']}"])
    run(*common, "--to=html5", "--output", str(html_file))

    # The PDF starts with the same illustrated cover used by the EPUB.
    cover = (f'<section class="book-cover">'
             f'<img src="{html_lib.escape(cover_png.resolve().as_uri())}" '
             f'alt="{html_lib.escape(title)} 表紙"/></section>')
    html_text = html_file.read_text(encoding="utf-8")
    if "<body>" not in html_text or 'id="TOC"' not in html_text:
        raise SystemExit("Unexpected Pandoc HTML structure: body/TOC absent")
    html_file.write_text(html_text.replace("<body>", "<body>\n" + cover + "\n", 1), encoding="utf-8")

    run(*common, "--to=epub3", "--split-level=1",
        "--epub-cover-image", str(cover_png),
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
