from __future__ import annotations

from .models import Paper


def _text_blob(paper: Paper) -> str:
    return " ".join(
        part for part in [paper.title, paper.abstract, paper.venue, " ".join(paper.authors)] if part
    ).lower()


def keyword_match(
    paper: Paper,
    include_keywords: list[str],
    exclude_keywords: list[str],
    required_keywords: list[str] | None = None,
    match_mode: str = "all",
) -> bool:
    blob = _text_blob(paper)
    required_keywords = required_keywords or []
    for group in required_keywords:
        alternatives = [item.strip().lower() for item in group.split("|") if item.strip()]
        if alternatives and not any(option in blob for option in alternatives):
            return False
    if include_keywords:
        matches = [keyword.lower() in blob for keyword in include_keywords]
        if match_mode == "any":
            if not any(matches):
                return False
        elif not all(matches):
            return False
    if exclude_keywords and any(keyword.lower() in blob for keyword in exclude_keywords):
        return False
    return True


def deduplicate(papers: list[Paper]) -> list[Paper]:
    seen_doi: set[str] = set()
    seen_title: set[str] = set()
    output: list[Paper] = []
    for paper in papers:
        doi = (paper.doi or "").strip().lower()
        title = paper.normalized_title()
        if doi and doi in seen_doi:
            continue
        if title and title in seen_title:
            continue
        if doi:
            seen_doi.add(doi)
        if title:
            seen_title.add(title)
        output.append(paper)
    return output


def flatten_search_terms(required_keywords: list[str], include_keywords: list[str]) -> list[str]:
    terms: list[str] = []
    for group in required_keywords:
        terms.extend(item.strip() for item in group.split("|") if item.strip())
    terms.extend(include_keywords)
    seen: set[str] = set()
    output: list[str] = []
    for term in terms:
        lowered = term.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        output.append(term)
    return output
