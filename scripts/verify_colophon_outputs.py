#!/usr/bin/env python3
"""Check the actual PDF/EPUB colophon against publication/imprint.json.

This is a *preview QA* check, not approval to publish. It detects an imprint
sharing the last PDF page with the References chapter and mismatched labels.
"""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from xml.etree import ElementTree
from zipfile import ZipFile

from pypdf import PdfReader

if __package__:
    from .check_release_readiness import unresolved_fields
else:
    from check_release_readiness import unresolved_fields

ROOT = Path(__file__).resolve().parents[1]


def expected_lines(imprint: dict[str, str]) -> tuple[str, ...]:
    day = date.fromisoformat(imprint["publication_date"])
    date_text = f"{day.year}年{day.month}月{day.day}日"
    planned = imprint["publication_status"] == "planned"
    return (
        "奥付（発行予定・校正用）" if planned else "奥付",
        f"著者：{imprint['author']}",
        f"発行：{imprint['publisher']}",
        f"{'発行予定日' if planned else '発行日'}：{date_text}",
        f"著作権表示：{imprint['copyright']}",
    )


def verify_pdf_pages(page_texts: list[str], imprint: dict[str, str]) -> None:
    if len(page_texts) < 3:
        raise ValueError("PDF has too few pages")
    if unresolved_fields(imprint):
        if "奥付（発行予定・校正用）" in page_texts[-1] or "著作権表示：" in page_texts[-1]:
            raise ValueError("Incomplete imprint should not be printed")
        return
    last = page_texts[-1]
    for value in expected_lines(imprint):
        if value not in last:
            raise ValueError(f"PDF final-page colophon missing: {value}")
    if "奥付" in page_texts[-2]:
        raise ValueError("Colophon begins on the preceding PDF page")
    if "ここに挙げた資料" in last or "参考資料" in last:
        raise ValueError("Colophon shares a PDF page with the references")
    if imprint["publication_status"] == "planned" and "発行日：" in last:
        raise ValueError("Planned preview must not claim an actual publication date")


def verify_epub(epub: Path, imprint: dict[str, str]) -> None:
    with ZipFile(epub) as archive:
        texts = []
        for name in archive.namelist():
            if name.endswith(".xhtml"):
                try:
                    root = ElementTree.fromstring(archive.read(name))
                except ElementTree.ParseError as exc:
                    raise ValueError(f"Invalid EPUB XHTML: {name}") from exc
                contents = "".join(root.itertext())
                if "奥付" in contents:
                    texts.append(contents)
    if unresolved_fields(imprint):
        if any("著作権表示：" in contents for contents in texts):
            raise ValueError("Incomplete imprint appeared in the EPUB")
        return
    # EPUB nav.xhtml also contains its TOC label. Only the separate
    # body chapter contains author, publisher, date, and copyright together.
    if not any(all(value in t for value in expected_lines(imprint)) for t in texts):
        raise ValueError("EPUB colophon does not match imprint.json")


def main() -> None:
    imprint = json.loads((ROOT / "publication/imprint.json").read_text(encoding="utf-8"))
    pdf = ROOT / "output/oss-book.pdf"
    epub = ROOT / "output/oss-book.epub"
    reader = PdfReader(pdf)
    pages = [(page.extract_text() or "") for page in reader.pages]
    verify_pdf_pages(pages, imprint)
    verify_epub(epub, imprint)
    print(f"Colophon QA passed: {len(pages)} PDF pages and EPUB3; "
          f"publication_status={imprint['publication_status']}")


if __name__ == "__main__":
    main()
