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

    writer.add_metadata({
        "/Title": "OSSを作る、OSSに育てられる — 試し読み",
        "/Author": "kawamurashingo",
        "/Subject": f"試し読み: 全{total}ページ中、冒頭{pages}ページ",
    })
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("wb") as fh:
        writer.write(fh)
    print(f"Sample: {destination} ({pages} / {total} pages)")
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
