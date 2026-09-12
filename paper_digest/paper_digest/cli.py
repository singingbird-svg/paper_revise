from __future__ import annotations

import argparse
import json
import os
from datetime import date, datetime
from pathlib import Path

from .filters import deduplicate, flatten_search_terms, keyword_match
from .gmail_source import fetch_gmail_alerts
from .models import Paper
from .report import render_markdown
from .sources import fetch_arxiv, fetch_crossref, fetch_ieee, fetch_openalex, fetch_semantic_scholar
from .summarizer import enrich_paper


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Collect and summarize daily papers from multiple sources.")
    parser.add_argument("--date", default="today", help="Target publication date, for example 2026-04-11 or today.")
    parser.add_argument("--config", default="", help="Optional JSON config file.")
    parser.add_argument("--keywords", default="", help="Comma-separated keywords that must all appear.")
    parser.add_argument(
        "--exclude-keywords",
        default="",
        help="Comma-separated keywords that must not appear.",
    )
    parser.add_argument("--max-per-source", type=int, default=20, help="Max records fetched from each source.")
    parser.add_argument(
        "--output",
        default="",
        help="Markdown output path. Defaults to reports/<date>.md",
    )
    return parser.parse_args()


def _parse_date(value: str) -> date:
    if value == "today":
        return date.today()
    return datetime.strptime(value, "%Y-%m-%d").date()


def _parse_keywords(raw: str) -> list[str]:
    return [item.strip() for item in raw.split(",") if item.strip()]


def _resolve_output_path(output_value: str, target_date: date) -> Path:
    if not output_value:
        return Path("reports") / f"{target_date.isoformat()}.md"
    return Path(output_value.format(date=target_date.isoformat()))


def collect_papers(
    target_date: date,
    include_keywords: list[str],
    exclude_keywords: list[str],
    required_keywords: list[str],
    keyword_match_mode: str,
    max_per_source: int,
    lookback_days: int,
    config: dict,
) -> list[Paper]:
    fetched: list[Paper] = []
    search_terms = flatten_search_terms(required_keywords, include_keywords)

    semantic_key = os.getenv(config.get("semantic_scholar_api_key_env", ""), "")
    ieee_key = os.getenv(config.get("ieee_api_key_env", ""), "")
    fetchers = [
        ("arXiv", lambda: fetch_arxiv(search_terms, target_date, max_per_source, lookback_days)),
        ("OpenAlex", lambda: fetch_openalex(search_terms, target_date, max_per_source, lookback_days)),
        ("Crossref", lambda: fetch_crossref(search_terms, target_date, max_per_source, lookback_days)),
        (
            "Semantic Scholar",
            lambda: fetch_semantic_scholar(search_terms, target_date, max_per_source, lookback_days, semantic_key),
        ),
        ("IEEE Xplore", lambda: fetch_ieee(search_terms, target_date, max_per_source, ieee_key, lookback_days)),
    ]
    gmail_config = config.get("gmail", {})
    if gmail_config.get("enabled"):
        fetchers.append(("Gmail Alerts", lambda: fetch_gmail_alerts(target_date, gmail_config)))

    for source_name, fetcher in fetchers:
        try:
            fetched.extend(fetcher())
        except Exception as exc:
            print(f"[warn] {source_name} failed: {exc}")

    filtered = [
        paper
        for paper in fetched
        if keyword_match(
            paper,
            include_keywords,
            exclude_keywords,
            required_keywords=required_keywords,
            match_mode=keyword_match_mode,
        )
    ]
    filtered = deduplicate(filtered)
    filtered.sort(key=lambda paper: (paper.published, paper.source, paper.title), reverse=True)
    return [enrich_paper(paper) for paper in filtered]


def main() -> int:
    args = parse_args()
    config = _load_config(args.config)
    raw_date = args.date if args.date != "today" or not config else config.get("date", args.date)
    raw_keywords = args.keywords if args.keywords or not config else config.get("keywords", "")
    raw_required = config.get("required_keywords", "")
    raw_excludes = args.exclude_keywords if args.exclude_keywords or not config else config.get("exclude_keywords", "")
    keyword_match_mode = str(config.get("keyword_match_mode", "all")).lower()
    max_per_source = args.max_per_source if args.max_per_source != 20 or not config else int(config.get("max_per_source", 20))
    lookback_days = int(config.get("lookback_days", 0))
    output_value = args.output if args.output or not config else config.get("output", "")
    target_date = _parse_date(raw_date)
    include_keywords = _parse_keywords(raw_keywords)
    required_keywords = _parse_keywords(raw_required)
    exclude_keywords = _parse_keywords(raw_excludes)

    papers = collect_papers(
        target_date=target_date,
        include_keywords=include_keywords,
        exclude_keywords=exclude_keywords,
        required_keywords=required_keywords,
        keyword_match_mode=keyword_match_mode,
        max_per_source=max_per_source,
        lookback_days=lookback_days,
        config=config,
    )

    output = _resolve_output_path(output_value, target_date)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        render_markdown(target_date.isoformat(), include_keywords, papers),
        encoding="utf-8",
    )
    print(f"Wrote {len(papers)} papers to {output}")
    return 0


def _load_config(path_value: str) -> dict:
    if not path_value:
        return {}
    return json.loads(Path(path_value).read_text(encoding="utf-8"))
