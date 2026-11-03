#!/usr/bin/env python3
"""Create a clearly labeled sample of the *already-built* publication PDF.

The sample uses original PDF pages rather than a separate Markdown manuscript,
so the cover, TOC and text always match the same build's full PDF.
This does not publish or upload the PDF to the marketplace.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from pypdf.generic import ArrayObject, NameObject, TextStringObject


def remove_dangling_named_links(writer: PdfWriter, reader: PdfReader, pages: int) -> int:
    """Remove links to chapters absent from the sample, retaining usable links.

    Pandoc's table of contents uses named destinations. pypdf retains link
    annotations when splitting pages but excludes destinations for omitted
    pages; those annotations would otherwise lead nowhere.
    """
    available = set()
    for name, destination in reader.named_destinations.items():
        try:
            target_page = reader.get_destination_page_number(destination)
        except (KeyError, ValueError):
            continue
        if 0 <= target_page < pages:
            available.add(name)

    removed = 0
    for page in writer.pages:
        original = page.get("/Annots")
        if not original:
            continue
        retained = ArrayObject()
        for ref in original:
            annotation = ref.get_object()
            destination = None
            if annotation.get("/Subtype") == "/Link":
                destination = annotation.get("/Dest")
                action = annotation.get("/A")
                if destination is None and action is not None and action.get("/S") == "/GoTo":
                    destination = action.get("/D")
            if isinstance(destination, (NameObject, TextStringObject)):
                if str(destination).lstrip("/") not in available:
                    removed += 1
                    continue
            retained.append(ref)
        if retained:
            page[NameObject("/Annots")] = retained
        else:
            page.pop(NameObject("/Annots"), None)
    return removed


def create_sample(source: Path, destination: Path, pages: int = 8) -> int:
    if source.resolve() == destination.resolve():
        raise ValueError("Sample output must not overwrite the full PDF")
    if pages < 1:
        raise ValueError("Sample page count must be positive")
    if not source.is_file():
        raise FileNotFoundError(f"Build the book first: {source}")
    reader = PdfReader(str(source))
    total = len(reader.pages)
    if total <= pages:
        raise ValueError(
            f"Refusing to distribute the entire manuscript as a sample "
            f"({total} total pages, requested {pages})"
        )

    writer = PdfWriter()
    for number in range(pages):
        writer.add_page(reader.pages[number])
    stripped = remove_dangling_named_links(writer, reader, pages)

    writer.add_metadata({
        "/Title": "OSSを作る、OSSに育てられる — 試し読み",
        "/Author": "kawamurashingo",
        "/Subject": f"試し読み: 全{total}ページ中、冒頭{pages}ページ",
    })
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("wb") as fh:
        writer.write(fh)
    print(f"Sample: {destination} ({pages} / {total} pages; {stripped} dangling TOC links removed)")
    return total


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path("output/oss-book.pdf"))
    parser.add_argument("--output", type=Path, default=Path("output/oss-book-sample.pdf"))
    parser.add_argument("--pages", type=int, default=8,
                        help="Number of front pages (default: 8)")
    args = parser.parse_args()
    create_sample(args.source, args.output, args.pages)


if __name__ == "__main__":
    main()
