from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Paper:
    source: str
    title: str
    abstract: str
    authors: list[str] = field(default_factory=list)
    url: str = ""
    published: str = ""
    doi: Optional[str] = None
    venue: str = ""
    summary_zh: str = ""
    innovation_zh: str = ""

    def normalized_title(self) -> str:
        return " ".join("".join(ch.lower() if ch.isalnum() else " " for ch in self.title).split())
