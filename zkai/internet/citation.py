"""CitationGenerator for web search citations."""

from typing import List
from zkai.internet.search_engine import SearchResult


class CitationGenerator:
    """Generates formatted academic and web citations for retrieved search sources."""

    @staticmethod
    def generate_citations(sources: List[SearchResult]) -> str:
        if not sources:
            return ""
        lines = ["\n### Web Citations"]
        for idx, src in enumerate(sources, 1):
            lines.append(f"[{idx}] {src.title}. Available: {src.url}")
        return "\n".join(lines)
