from django.test import SimpleTestCase

from horilla.export_safety import safe_row


class SafeRowTest(SimpleTestCase):
    def test_every_string_cell_is_neutralised(self):
        self.assertEqual(
            safe_row(['=HYPERLINK("http://x")', 2, "ok", None, "-5"]),
            ["'=HYPERLINK(\"http://x\")", 2, "ok", "", "'-5"],
        )

    def test_no_trigger_leaves_text_alone(self):
        self.assertEqual(safe_row(["Acme Ltd", "2026-01-31"]), ["Acme Ltd", "2026-01-31"])
