from __future__ import annotations

from collections import defaultdict

from .models import Paper


def render_markdown(date_text: str, keywords: list[str], papers: list[Paper]) -> str:
    grouped: dict[str, list[Paper]] = defaultdict(list)
    for paper in papers:
        grouped[paper.source].append(paper)

    lines: list[str] = []
    lines.append(f"# 文献日报 - {date_text}")
    lines.append("")
    if keywords:
        lines.append(f"关键词：`{', '.join(keywords)}`")
        lines.append("")
    lines.append(f"共筛出 **{len(papers)}** 篇论文。")
    lines.append("")

    for source in sorted(grouped):
        lines.append(f"## {source}")
        lines.append("")
        for idx, paper in enumerate(grouped[source], start=1):
            lines.append(f"### {idx}. {paper.title}")
            lines.append("")
            meta = [
                f"来源：{paper.source}",
                f"日期：{paper.published or '未知'}",
            ]
            if paper.venue:
                meta.append(f"期刊/会议信息：{paper.venue}")
            if paper.doi:
                meta.append(f"DOI：{paper.doi}")
            lines.append("；".join(meta))
            lines.append("")
            if paper.authors:
                lines.append(f"作者：{', '.join(paper.authors[:8])}")
                lines.append("")
            lines.append(f"链接：{paper.url or '无'}")
            lines.append("")
            lines.append(f"摘要总结：{paper.summary_zh}")
            lines.append("")
            lines.append(f"主要创新点：{paper.innovation_zh}")
            lines.append("")
        lines.append("")

    return "\n".join(lines).strip() + "\n"
