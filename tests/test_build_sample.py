import tempfile
import unittest
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from pypdf.generic import ArrayObject, DictionaryObject, NameObject, NumberObject, TextStringObject
from scripts.build_sample import create_sample


class SamplePdfTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.src = Path(self.tmp.name) / "full.pdf"
        self.dest = Path(self.tmp.name) / "sample.pdf"
        writer = PdfWriter()
        for _ in range(12):
            writer.add_blank_page(width=420, height=595)
        with self.src.open("wb") as f:
            writer.write(f)

    def test_keeps_first_pages_in_order(self):
        self.assertEqual(create_sample(self.src, self.dest, 8), 12)
        result = PdfReader(str(self.dest))
        self.assertEqual(len(result.pages), 8)
        self.assertEqual(result.metadata.title, "OSSを作る、OSSに育てられる — 試し読み")
        self.assertEqual(float(result.pages[0].mediabox.width), 420)

    def test_removes_only_links_to_pages_outside_sample(self):
        writer = PdfWriter()
        for _ in range(12):
            writer.add_blank_page(width=420, height=595)
        writer.add_named_destination("inside", 2)
        writer.add_named_destination("outside", 11)

        def link(destination=None, url=None):
            a = DictionaryObject({
                NameObject("/Type"): NameObject("/Annot"),
                NameObject("/Subtype"): NameObject("/Link"),
                NameObject("/Rect"): ArrayObject([
                    NumberObject(0), NumberObject(0),
                    NumberObject(40), NumberObject(20),
                ]),
            })
            if destination is not None:
                a[NameObject("/Dest")] = TextStringObject(destination)
            else:
                a[NameObject("/A")] = DictionaryObject({
                    NameObject("/S"): NameObject("/URI"),
                    NameObject("/URI"): TextStringObject(url),
                })
            return writer._add_object(a)

        writer.pages[1][NameObject("/Annots")] = ArrayObject([
            link(destination="inside"),
            link(destination="outside"),
            link(url="https://example.org"),
        ])
        with self.src.open("wb") as f:
            writer.write(f)

        create_sample(self.src, self.dest, 8)
        sample = PdfReader(str(self.dest))
        annotations = [ref.get_object() for ref in sample.pages[1]["/Annots"]]
        self.assertEqual(len(annotations), 2)
        self.assertEqual(annotations[0]["/Dest"], "inside")
        self.assertEqual(annotations[1]["/A"]["/URI"], "https://example.org")
        self.assertIn("inside", sample.named_destinations)
        self.assertNotIn("outside", sample.named_destinations)

    def test_rejects_accidental_full_book(self):
        with self.assertRaisesRegex(ValueError, "entire manuscript"):
            create_sample(self.src, self.dest, 12)
        self.assertFalse(self.dest.exists())

    def test_rejects_overwrite(self):
        with self.assertRaisesRegex(ValueError, "overwrite"):
            create_sample(self.src, self.src, 2)

    def test_rejects_invalid_page_count(self):
        with self.assertRaises(ValueError):
            create_sample(self.src, self.dest, 0)


if __name__ == "__main__":
    unittest.main()
