import unittest

from scripts.verify_colophon_outputs import expected_lines, verify_pdf_pages

PLANNED = {
    "author": "kawamurashingo",
    "publisher": "知つなぐ舎",
    "publication_date": "2026-11-21",
    "copyright": "© 2026 kawamurashingo",
    "publication_status": "planned",
}


class ColophonQualityTests(unittest.TestCase):
    def test_planned_colophon_on_clean_final_page(self):
        page = "\n".join(expected_lines(PLANNED))
        verify_pdf_pages(["cover", "参考資料", page], PLANNED)

    def test_references_and_colophon_must_be_separate(self):
        page = "ここに挙げた資料は... \n" + "\n".join(expected_lines(PLANNED))
        with self.assertRaisesRegex(ValueError, "shares a PDF page"):
            verify_pdf_pages(["cover", "参考資料", page], PLANNED)

    def test_planned_issue_cannot_claim_publication(self):
        page = "\n".join(expected_lines(PLANNED)) + "\n発行日：2026年11月21日"
        with self.assertRaisesRegex(ValueError, "actual publication date"):
            verify_pdf_pages(["cover", "参考資料", page], PLANNED)

    def test_missing_last_page_metadata_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "missing"):
            verify_pdf_pages(["cover", "参考資料", "奥付"], PLANNED)


if __name__ == "__main__":
    unittest.main()
