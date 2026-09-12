import unittest

from datetime import date

from paper_digest.filters import deduplicate, flatten_search_terms, keyword_match
from paper_digest.models import Paper
from paper_digest.cli import _resolve_output_path


class FilterTests(unittest.TestCase):
    def test_keyword_match_include_and_exclude(self) -> None:
        paper = Paper(source="x", title="Multi-agent planning", abstract="Task allocation with LTL constraints")
        self.assertTrue(keyword_match(paper, ["multi-agent", "ltl"], ["biology"]))
        self.assertFalse(keyword_match(paper, ["robot"], []))
        self.assertFalse(keyword_match(paper, ["ltl"], ["allocation"]))

    def test_keyword_match_any_mode(self) -> None:
        paper = Paper(source="x", title="Multi-agent planning", abstract="Task allocation with LTL constraints")
        self.assertTrue(keyword_match(paper, ["robot", "ltl"], [], match_mode="any"))
        self.assertFalse(keyword_match(paper, ["robot", "vision"], [], match_mode="any"))

    def test_keyword_match_required_keywords(self) -> None:
        paper = Paper(source="x", title="Temporal logic for multi-robot planning", abstract="Task allocation")
        self.assertTrue(keyword_match(paper, ["multi-robot"], [], required_keywords=["temporal logic"], match_mode="any"))
        self.assertFalse(keyword_match(paper, ["multi-robot"], [], required_keywords=["formal methods"], match_mode="any"))

    def test_keyword_match_required_keyword_group(self) -> None:
        paper = Paper(source="x", title="LTL for multi-robot planning", abstract="Task allocation")
        self.assertTrue(keyword_match(paper, ["multi-robot"], [], required_keywords=["temporal logic|ltl"], match_mode="any"))
        self.assertFalse(keyword_match(paper, ["multi-robot"], [], required_keywords=["signal temporal logic|metric temporal logic"], match_mode="any"))

    def test_deduplicate_by_title_and_doi(self) -> None:
        papers = [
            Paper(source="a", title="Same Title", abstract="", doi="10.1/abc"),
            Paper(source="b", title="Same Title", abstract="", doi="10.1/abc"),
            Paper(source="c", title="Same Title", abstract=""),
        ]
        deduped = deduplicate(papers)
        self.assertEqual(len(deduped), 1)

    def test_resolve_output_path_expands_date_placeholder(self) -> None:
        output = _resolve_output_path("reports/{date}.md", date(2026, 4, 12))
        self.assertEqual(str(output), "reports/2026-04-12.md")

    def test_flatten_search_terms_includes_required_alternatives(self) -> None:
        terms = flatten_search_terms(["temporal logic|ltl"], ["multi-robot"])
        self.assertEqual(terms, ["temporal logic", "ltl", "multi-robot"])


if __name__ == "__main__":
    unittest.main()
