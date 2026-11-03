import unittest

from scripts.check_release_readiness import release_blockers, unresolved_fields
from scripts.build_release import complete_imprint, make_colophon


def imprint(**changes):
    data = {
        "author": "kawamurashingo",
        "publisher": "知つなぐ舎",
        "publication_date": "2026-11-21",
        "publication_status": "planned",
        "copyright": "© 2026 kawamurashingo",
        "contact": "",
    }
    data.update(changes)
    return data


class PublicationReadinessTests(unittest.TestCase):
    def test_missing_fields_are_reported(self):
        result = unresolved_fields(imprint(publication_date="", copyright=""))
        self.assertEqual(result, ["発行予定日／発行日 (publication_date)", "著作権表示 (copyright)"])

    def test_complete_planned_metadata_but_not_released(self):
        self.assertEqual(unresolved_fields(imprint()), [])
        self.assertTrue(complete_imprint(imprint()))
        self.assertEqual(release_blockers(imprint()),
                         ["発行は未実施・日付は予定 (publication_status)"])

    def test_published_is_potentially_ready_for_release_audit(self):
        self.assertEqual(release_blockers(imprint(publication_status="published")), [])

    def test_rejects_placeholder(self):
        data = imprint(author="TBD", publisher="未確定", publication_date="未定", copyright="TODO")
        self.assertEqual(len(unresolved_fields(data)), 4)
        self.assertFalse(complete_imprint(data))

    def test_rejects_wrong_types(self):
        with self.assertRaises(ValueError):
            unresolved_fields(imprint(author=123))

    def test_rejects_missing_status(self):
        data = imprint()
        del data["publication_status"]
        self.assertIn("発行状態 (publication_status)", unresolved_fields(data))
        self.assertFalse(complete_imprint(data))

    def test_rejects_invalid_issue_date(self):
        data = imprint(publication_date="2026-11-31")
        self.assertIn("発行日（YYYY-MM-DD形式が必要） (publication_date)",
                      unresolved_fields(data))
        self.assertFalse(complete_imprint(data))

    def test_planned_colophon_is_not_false_publication_claim(self):
        body = make_colophon(imprint(), "OSSを作る、OSSに育てられる")
        self.assertIn("# 奥付（発行予定・校正用）", body)
        self.assertIn("発行予定日：2026年11月21日", body)
        self.assertIn("著作権表示：© 2026 kawamurashingo", body)
        self.assertNotIn("\n\n発行日：", body)

    def test_published_colophon_uses_actual_date_label(self):
        body = make_colophon(imprint(publication_status="published"), "本")
        self.assertTrue(body.startswith("# 奥付\n"))
        self.assertIn("発行日：2026年11月21日", body)
        self.assertNotIn("発行予定日：", body)


if __name__ == "__main__":
    unittest.main()
