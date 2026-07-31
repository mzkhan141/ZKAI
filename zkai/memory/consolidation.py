"""Memory Consolidation, Automatic Forgetting, Decay, and Merging."""

from datetime import datetime
from typing import List
from zkai.memory.base import MemoryEntry
from zkai.memory.ranking import ImportanceScorer
from zkai.core.logger import get_logger

logger = get_logger("memory.consolidation")


class MemoryDecay:
    """Evaluates memory decay factors and identifies stale memories for purging."""

    @staticmethod
    def is_stale(entry: MemoryEntry, threshold: float = 0.01) -> bool:
        score = ImportanceScorer.calculate_score(entry)
        return score < threshold


class MemoryMerger:
    """Merges duplicate or overlapping memory entries."""

    @staticmethod
    def merge_entries(e1: MemoryEntry, e2: MemoryEntry) -> MemoryEntry:
        merged_content = f"{e1.content}\n{e2.content}"
        e1.content = merged_content
        e1.metadata.importance_score = max(e1.metadata.importance_score, e2.metadata.importance_score) + 0.2
        return e1


class MemoryConsolidator:
    """Consolidates short-term memories into long-term structures while purging stale items."""

    def __init__(self, decay_threshold: float = 0.05):
        self.decay_threshold = decay_threshold

    def consolidate(self, short_term_entries: List[MemoryEntry]) -> tuple[List[MemoryEntry], List[MemoryEntry]]:
        """Splits short term memories into (important_for_long_term, stale_for_forgetting)."""
        keep = []
        purge = []

        for entry in short_term_entries:
            if MemoryDecay.is_stale(entry, threshold=self.decay_threshold):
                purge.append(entry)
            else:
                keep.append(entry)

        logger.info(f"Consolidated memory: Kept {len(keep)}, Purged {len(purge)} stale entries")
        return keep, purge
