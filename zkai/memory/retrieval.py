"""Unified Memory Retrieval Engine combining semantic search and rankers."""

from typing import List, Dict, Any
from zkai.memory.base import MemoryEntry, BaseMemory
from zkai.memory.ranking import MemoryRanker
from zkai.core.logger import get_logger

logger = get_logger("memory.retrieval")


class MemoryRetriever:
    """Unified Retriever executing parallel queries across multi-tier memory stores."""

    def __init__(self, memory_stores: List[BaseMemory]):
        self.stores = memory_stores

    def search(self, query: str, top_k: int = 5) -> List[MemoryEntry]:
        """Searches all registered memory subsystems and returns ranked results."""
        all_matches: List[MemoryEntry] = []
        for store in self.stores:
            try:
                results = store.retrieve(query, top_k=top_k)
                all_matches.extend(results)
            except Exception as e:
                logger.error(f"Error querying memory store '{store.memory_type.value}': {e}")

        # Rank candidates using combined importance & recency scoring
        ranked = MemoryRanker.rank(all_matches)
        return ranked[:top_k]
