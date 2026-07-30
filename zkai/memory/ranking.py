"""Memory Ranking and Importance Scoring algorithms."""

from datetime import datetime
import math
from typing import List, Optional
from zkai.memory.base import MemoryEntry


class ImportanceScorer:
    """Calculates dynamic relevance and importance scores for memory entries."""

    @staticmethod
    def calculate_score(entry: MemoryEntry, current_time: Optional[datetime] = None) -> float:
        now = current_time or datetime.now()
        age_hours = max(0.0, (now - entry.metadata.created_at).total_seconds() / 3600.0)

        recency_decay = math.exp(-entry.metadata.decay_factor * age_hours)
        frequency_boost = math.log1p(entry.metadata.access_count)

        return entry.metadata.importance_score * recency_decay * (1.0 + frequency_boost)


class MemoryRanker:
    """Ranks memory entries based on combined similarity, recency, and importance scores."""

    @staticmethod
    def rank(entries: List[MemoryEntry]) -> List[MemoryEntry]:
        return sorted(entries, key=ImportanceScorer.calculate_score, reverse=True)
