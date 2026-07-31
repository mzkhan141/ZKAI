"""CitationEngine generating citations and attribution links."""

from dataclasses import dataclass
from typing import List


@dataclass
class Citation:
    source_title: str
    uri_or_path: str
    snippet: str
    index: int


class CitationEngine:
    """Formats and appends bibliographic citations to generated texts."""

    @staticmethod
    def format_citations(citations: List[Citation]) -> str:
        if not citations:
            return ""
        formatted = ["\n\n--- References & Sources ---"]
        for c in citations:
            formatted.append(f"[{c.index}] {c.source_title} - {c.uri_or_path}\n    \"{c.snippet[:100]}...\"")
        return "\n".join(formatted)
