import unittest

from paper_digest.sources import _extract_openalex_venue


class OpenAlexSourceTests(unittest.TestCase):
    def test_extract_openalex_venue_handles_null_source(self) -> None:
        item = {"primary_location": {"source": None}}
        self.assertEqual(_extract_openalex_venue(item), "")

    def test_extract_openalex_venue_reads_display_name(self) -> None:
        item = {"primary_location": {"source": {"display_name": "ICRA"}}}
        self.assertEqual(_extract_openalex_venue(item), "ICRA")


if __name__ == "__main__":
    unittest.main()
