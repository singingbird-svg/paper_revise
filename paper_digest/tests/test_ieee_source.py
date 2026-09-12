import unittest

from paper_digest.sources import _extract_ieee_date


class IeeeSourceTests(unittest.TestCase):
    def test_extract_ieee_date_variants(self) -> None:
        self.assertEqual(_extract_ieee_date({"publication_date": "12 April 2026"}), "2026-04-12")
        self.assertEqual(_extract_ieee_date({"publication_date": "Apr 12, 2026"}), "2026-04-12")
        self.assertEqual(_extract_ieee_date({"publication_year": "2026"}), "2026-01-01")


if __name__ == "__main__":
    unittest.main()
