import tempfile
import unittest
from pathlib import Path

from pypdf import PdfReader, PdfWriter
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
