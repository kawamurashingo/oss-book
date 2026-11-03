import unittest

from scripts.check_release_readiness import unresolved_fields
from scripts.build_release import complete_imprint


class PublicationReadinessTests(unittest.TestCase):
    def test_missing_fields_are_reported(self):
        result = unresolved_fields({
            "author": "kawamurashingo",
            "publisher": "知つなぐ舎",
            "publication_date": "",
            "copyright": "",
        })
        self.assertEqual(result, ["発行日 (publication_date)", "著作権表示 (copyright)"])

    def test_complete_metadata(self):
        self.assertEqual(unresolved_fields({
            "author": "test-author",
            "publisher": "test-publisher",
            "publication_date": "2099-01-01",
            "copyright": "Copyright test-author",
        }), [])

    def test_rejects_placeholder(self):
        data = {"author": "TBD", "publisher": "未確定", "publication_date": "未定", "copyright": "TODO"}
        self.assertEqual(len(unresolved_fields(data)), 4)

    def test_build_never_emits_placeholder_colophon(self):
        metadata = {
            "author": "kawamurashingo",
            "publisher": "知つなぐ舎",
            "publication_date": "未確定",
            "copyright": "TBD",
        }
        self.assertFalse(complete_imprint(metadata))

    def test_build_and_audit_agree_when_complete(self):
        metadata = {
            "author": "kawamurashingo",
            "publisher": "知つなぐ舎",
            "publication_date": "2099-01-01",
            "copyright": "Copyright test-author",
        }
        self.assertTrue(complete_imprint(metadata))

    def test_rejects_wrong_types(self):
        with self.assertRaises(ValueError):
            unresolved_fields({"author": 123})


if __name__ == "__main__":
    unittest.main()
