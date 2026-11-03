"""Confirm that the excerpt is an exact, ordered prefix of the real manuscript."""
import unittest
from pathlib import Path

from scripts.build_sample import ROOT, SAMPLE_FILENAMES, sample_markdown


class SampleIntegrityTests(unittest.TestCase):
    def test_exact_original_chapters(self):
        expected = "\n\n".join(
            (ROOT / "manuscript" / name).read_text(encoding="utf-8").rstrip()
            for name in SAMPLE_FILENAMES
        ) + "\n"
        self.assertEqual(sample_markdown(), expected)

    def test_full_chapter_boundaries(self):
        content = sample_markdown()
        headings = [line for line in content.splitlines() if line.startswith("# ")]
        self.assertEqual(len(headings), len(SAMPLE_FILENAMES))
        self.assertTrue(headings[0].startswith("# はじめに"))
        self.assertIn("第2章", headings[-1])
        self.assertNotIn("# 第3章", content)
        self.assertNotIn("# 参考資料", content)

    def test_no_invented_metadata(self):
        text = sample_markdown()
        self.assertNotIn("# 奥付", text)
        self.assertNotIn("著作権表示：", text)


if __name__ == "__main__":
    unittest.main()
