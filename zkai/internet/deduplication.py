"""ContentDeduplicator for web content."""

from typing import List


class ContentDeduplicator:
    """Deduplicates web search text snippets using hash signatures."""

    @staticmethod
    def deduplicate(texts: List[str]) -> List[str]:
        seen = set()
        unique = []
        for text in texts:
            cleaned = " ".join(text.split())
            if cleaned not in seen:
                seen.add(cleaned)
                unique.append(text)
        return unique
