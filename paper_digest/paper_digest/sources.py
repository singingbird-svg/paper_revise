from __future__ import annotations

import json
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date
from urllib.error import HTTPError

from .models import Paper


USER_AGENT = "paper-digest/0.1 (mailto:local-user@example.com)"


def _http_get_json(url: str) -> dict:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def _http_get_text(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8")


def _same_day(candidate: str, target: date) -> bool:
    return candidate[:10] == target.isoformat()


def _within_days(candidate: str, target: date, lookback_days: int) -> bool:
    if not candidate:
        return False
    try:
        candidate_date = date.fromisoformat(candidate[:10])
    except ValueError:
        return False
    delta = (target - candidate_date).days
    return 0 <= delta <= lookback_days


def fetch_arxiv(keywords: list[str], target_date: date, max_results: int, lookback_days: int = 0) -> list[Paper]:
    search = " OR ".join(f'all:"{keyword}"' for keyword in keywords) if keywords else "all:*"
    params = {
        "search_query": search,
        "start": "0",
        "max_results": str(max_results),
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }
    url = "http://export.arxiv.org/api/query?" + urllib.parse.urlencode(params)
    xml_text = _http_get_text(url)
    root = ET.fromstring(xml_text)
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    papers: list[Paper] = []
    for entry in root.findall("atom:entry", ns):
        published = entry.findtext("atom:published", default="", namespaces=ns)
        if published and not _within_days(published, target_date, lookback_days):
            continue
        authors = [node.findtext("atom:name", default="", namespaces=ns) for node in entry.findall("atom:author", ns)]
        title = " ".join(entry.findtext("atom:title", default="", namespaces=ns).split())
        summary = " ".join(entry.findtext("atom:summary", default="", namespaces=ns).split())
        papers.append(
            Paper(
                source="arXiv",
                title=title,
                abstract=summary,
                authors=[a for a in authors if a],
                url=entry.findtext("atom:id", default="", namespaces=ns),
                published=published[:10],
            )
        )
    return papers


def fetch_openalex(keywords: list[str], target_date: date, max_results: int, lookback_days: int = 0) -> list[Paper]:
    start_date = target_date.fromordinal(target_date.toordinal() - lookback_days)
    params = {
        "per-page": str(max_results),
        "filter": f"from_publication_date:{start_date.isoformat()},to_publication_date:{target_date.isoformat()}",
        "sort": "publication_date:desc",
    }
    if keywords:
        params["search"] = " ".join(keywords)
    url = "https://api.openalex.org/works?" + urllib.parse.urlencode(params)
    payload = _http_get_json(url)
    papers: list[Paper] = []
    for item in payload.get("results", []):
        abstract_index = item.get("abstract_inverted_index") or {}
        abstract = _rebuild_openalex_abstract(abstract_index)
        authors = [
            authorship.get("author", {}).get("display_name", "")
            for authorship in item.get("authorships", [])
            if authorship.get("author", {}).get("display_name")
        ]
        papers.append(
            Paper(
                source="OpenAlex",
                title=item.get("display_name", "").strip(),
                abstract=abstract,
                authors=authors,
                url=item.get("id", ""),
                published=item.get("publication_date", "") or "",
                doi=item.get("doi"),
                venue=_extract_openalex_venue(item),
            )
        )
    return papers


def _rebuild_openalex_abstract(index: dict) -> str:
    if not index:
        return ""
    positions: list[tuple[int, str]] = []
    for word, slots in index.items():
        for slot in slots:
            positions.append((slot, word))
    positions.sort(key=lambda item: item[0])
    return " ".join(word for _, word in positions)


def _extract_openalex_venue(item: dict) -> str:
    primary_location = item.get("primary_location") or {}
    source = primary_location.get("source") or {}
    if isinstance(source, dict):
        return source.get("display_name", "") or ""
    return ""


def fetch_crossref(keywords: list[str], target_date: date, max_results: int, lookback_days: int = 0) -> list[Paper]:
    start_date = target_date.fromordinal(target_date.toordinal() - lookback_days)
    params = {
        "rows": str(max_results),
        "filter": f"from-pub-date:{start_date.isoformat()},until-pub-date:{target_date.isoformat()}",
        "sort": "published",
        "order": "desc",
    }
    if keywords:
        params["query"] = " ".join(keywords)
    url = "https://api.crossref.org/works?" + urllib.parse.urlencode(params)
    payload = _http_get_json(url)
    papers: list[Paper] = []
    for item in payload.get("message", {}).get("items", []):
        title = " ".join((item.get("title") or [""])[:1]).strip()
        abstract = _strip_jats(item.get("abstract", "") or "")
        authors = []
        for author in item.get("author", []):
            given = author.get("given", "")
            family = author.get("family", "")
            full_name = " ".join(part for part in [given, family] if part).strip()
            if full_name:
                authors.append(full_name)
        papers.append(
            Paper(
                source="Crossref",
                title=title,
                abstract=abstract,
                authors=authors,
                url=(item.get("URL") or ""),
                published=_extract_crossref_date(item),
                doi=item.get("DOI"),
                venue=" ".join((item.get("container-title") or [""])[:1]).strip(),
            )
        )
    return papers


def fetch_semantic_scholar(
    keywords: list[str],
    target_date: date,
    max_results: int,
    lookback_days: int = 0,
    api_key: str = "",
) -> list[Paper]:
    params = {
        "query": " ".join(keywords),
        "limit": str(max_results),
        "fields": "title,abstract,authors,externalIds,url,publicationDate,venue",
    }
    if not params["query"].strip():
        return []
    params["year"] = str(target_date.year)
    url = "https://api.semanticscholar.org/graph/v1/paper/search?" + urllib.parse.urlencode(params)
    payload = _semantic_request(url, api_key)

    papers: list[Paper] = []
    for item in payload.get("data", []):
        published = item.get("publicationDate", "") or ""
        if published and not _within_days(published, target_date, lookback_days):
            continue
        papers.append(
            Paper(
                source="Semantic Scholar",
                title=item.get("title", "").strip(),
                abstract=item.get("abstract", "") or "",
                authors=[author.get("name", "") for author in item.get("authors", []) if author.get("name")],
                url=item.get("url", ""),
                published=published[:10] if published else "",
                doi=(item.get("externalIds") or {}).get("DOI"),
                venue=item.get("venue", "") or "",
            )
        )
    return papers


def fetch_ieee(
    keywords: list[str],
    target_date: date,
    max_results: int,
    api_key: str = "",
    lookback_days: int = 0,
) -> list[Paper]:
    if not api_key or not keywords:
        return []

    querytext = "(" + " OR ".join(f'"{keyword}"' for keyword in keywords) + ")"
    params = {
        "apikey": api_key,
        "querytext": querytext,
        "max_records": str(min(max_results, 200)),
        "start_record": "1",
        "format": "json",
    }
    url = "https://ieeexploreapi.ieee.org/api/v1/search/articles?" + urllib.parse.urlencode(params)
    payload = _http_get_json(url)

    papers: list[Paper] = []
    for item in payload.get("articles", []):
        published = _extract_ieee_date(item)
        if published and not _within_days(published, target_date, lookback_days):
            continue

        authors = []
        for author in (item.get("authors") or {}).get("authors", []):
            name = author.get("full_name", "") or ""
            if name:
                authors.append(name)

        papers.append(
            Paper(
                source="IEEE Xplore",
                title=item.get("title", "").strip(),
                abstract=item.get("abstract", "") or "",
                authors=authors,
                url=item.get("html_url") or item.get("abstract_url") or "",
                published=published,
                doi=item.get("doi"),
                venue=item.get("publication_title", "") or "",
            )
        )
    return papers


def _semantic_request(url: str, api_key: str) -> dict:
    delays = [1.0, 2.0, 4.0]
    for attempt, delay in enumerate(delays, start=1):
        request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        if api_key:
            request.add_header("x-api-key", api_key)
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            if exc.code != 429 or attempt == len(delays):
                raise
            time.sleep(delay)
    return {}


def _strip_jats(text: str) -> str:
    return " ".join(
        ET.fromstring(f"<root>{text}</root>").itertext()
    ).strip() if text else ""


def _extract_crossref_date(item: dict) -> str:
    date_parts = item.get("published", {}).get("date-parts") or item.get("published-print", {}).get("date-parts")
    if not date_parts:
        return ""
    parts = date_parts[0]
    parts = parts + [1] * (3 - len(parts))
    return f"{parts[0]:04d}-{parts[1]:02d}-{parts[2]:02d}"


def _extract_ieee_date(item: dict) -> str:
    raw = item.get("publication_date", "") or ""
    if not raw:
        year = item.get("publication_year")
        return f"{int(year):04d}-01-01" if year else ""

    raw = raw.strip()
    formats = [
        "%d %B %Y",
        "%d %b %Y",
        "%B %d, %Y",
        "%b %d, %Y",
        "%Y-%m-%d",
    ]
    from datetime import datetime

    for fmt in formats:
        try:
            return datetime.strptime(raw, fmt).date().isoformat()
        except ValueError:
            continue
    if len(raw) == 4 and raw.isdigit():
        return f"{raw}-01-01"
    return ""
