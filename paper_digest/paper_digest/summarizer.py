from __future__ import annotations

import re

from .models import Paper

INNOVATION_CUES = [
    "we propose",
    "we present",
    "we introduce",
    "we develop",
    "we design",
    "this paper proposes",
    "this paper presents",
    "our contribution",
    "our contributions",
    "novel",
]


def _split_sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+|\n+", text.strip())
    return [part.strip() for part in parts if part.strip()]


def _compress_summary(text: str) -> str:
    sentences = _split_sentences(text)
    if not sentences:
        return "未提供摘要。"
    chosen = " ".join(sentences[:2])
    return f"本文主要讨论：{chosen}"


def _extract_innovation(text: str) -> str:
    sentences = _split_sentences(text)
    lowered = text.lower()
    for cue in INNOVATION_CUES:
        if cue in lowered:
            for sentence in sentences:
                if cue in sentence.lower():
                    return f"可能的创新点：{sentence}"
    if sentences:
        return f"可能的创新点：{sentences[0]}"
    return "可能的创新点：摘要缺失，暂无法自动提炼。"


def enrich_paper(paper: Paper) -> Paper:
    abstract = (paper.abstract or "").strip()
    paper.summary_zh = _compress_summary(abstract)
    paper.innovation_zh = _extract_innovation(abstract)
    return paper
