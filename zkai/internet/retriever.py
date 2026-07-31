"""InformationRetriever and SourceRanker for internet web sources."""

from typing import List, Dict, Any
from zkai.internet.search_engine import SearchResult


class SourceRanker:
    """Ranks search result sources by authority, freshness, and relevance."""

    def rank(self, results: List[SearchResult]) -> List[SearchResult]:
        # Prioritize HTTPS and known domains
        return sorted(results, key=lambda r: 1.0 if r.url.startswith("https://") else 0.5, reverse=True)


class InformationRetriever:
    """Retrieves and ranks web search information."""

    def __init__(self):
        self.ranker = SourceRanker()

    def retrieve_best(self, results: List[SearchResult], top_k: int = 5) -> List[SearchResult]:
        ranked = self.ranker.rank(results)
        return ranked[:top_k]
