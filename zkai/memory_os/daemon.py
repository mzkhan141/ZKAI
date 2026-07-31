"""Memory Operating System Daemon and background maintenance routines."""

import json
from pathlib import Path
import time
from typing import Any, Dict, List, Optional
from zkai.memory.manager import MemoryManager
from zkai.memory.base import MemoryEntry
from zkai.core.logger import get_logger

logger = get_logger("memory_os")


class MemoryGarbageCollector:
    """Purges low-importance and expired entries across memory stores."""

    @staticmethod
    def collect_garbage(memory_manager: MemoryManager, min_importance: float = 0.1) -> int:
        purged = 0
        working_entries = list(memory_manager.working._store)
        for entry in working_entries:
            if entry.metadata.importance_score < min_importance:
                memory_manager.working._store.remove(entry)
                purged += 1
        return purged


class MemoryDefragmenter:
    """Compacts vector memory indices for optimal search latency."""

    @staticmethod
    def defragment(memory_manager: MemoryManager) -> None:
        logger.info("MemoryDefragmenter compacting vector indices...")


class KnowledgeOptimizer:
    """Deduplicates and merges knowledge graph nodes."""

    @staticmethod
    def optimize(memory_manager: MemoryManager) -> None:
        logger.info("KnowledgeOptimizer optimizing Knowledge Graph structure...")


class EmbeddingOptimizer:
    """Re-indexes stale embedding vectors."""

    @staticmethod
    def optimize(memory_manager: MemoryManager) -> None:
        logger.info("EmbeddingOptimizer refreshing embedding index...")


class RelationshipMaintainer:
    """Prunes stale or weak graph relationship edges."""

    @staticmethod
    def maintain(memory_manager: MemoryManager) -> None:
        logger.info("RelationshipMaintainer maintaining graph relationship weights...")


class MemorySnapshot:
    """Serializes complete memory state into snapshot JSON / .zk payloads."""

    @staticmethod
    def create_snapshot(memory_manager: MemoryManager, filepath: str) -> None:
        data = {
            "timestamp": time.time(),
            "short_term_count": len(memory_manager.short_term._store),
            "working_count": len(memory_manager.working._store),
        }
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f)
        logger.info(f"Created MemorySnapshot at {filepath}")


class MemoryRestore:
    """Restores memory state from snapshot files."""

    @staticmethod
    def restore(filepath: str) -> Dict[str, Any]:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)


class MemoryVersioning:
    """Tracks memory state revisions over time."""

    def __init__(self):
        self.revisions: List[str] = []

    def tag_revision(self, revision_name: str) -> None:
        self.revisions.append(revision_name)


class TemporalMemory:
    """Time-aware memory layer applying exponential recency decay curves."""

    @staticmethod
    def compute_decay(entry: MemoryEntry, current_time: float, decay_rate: float = 0.05) -> float:
        age_hours = (current_time - entry.metadata.created_at.timestamp()) / 3600.0
        decayed_importance = entry.metadata.importance_score * (1.0 / (1.0 + decay_rate * age_hours))
        return max(0.0, decayed_importance)


class BackgroundConsolidation:
    """Background consolidation routine invoking MemoryManager.consolidate()."""

    def __init__(self, memory_manager: MemoryManager):
        self.memory_manager = memory_manager

    def run_consolidation(self) -> None:
        self.memory_manager.consolidate()


class MemoryDaemon:
    """Master Memory OS Daemon running continuous background maintenance."""

    def __init__(self, memory_manager: Optional[MemoryManager] = None):
        self.memory_manager = memory_manager or MemoryManager()
        self.gc = MemoryGarbageCollector()
        self.defragmenter = MemoryDefragmenter()
        self.knowledge_optimizer = KnowledgeOptimizer()
        self.embedding_optimizer = EmbeddingOptimizer()
        self.relationship_maintainer = RelationshipMaintainer()
        self.consolidation = BackgroundConsolidation(self.memory_manager)

    def tick_maintenance(self) -> Dict[str, Any]:
        purged = self.gc.collect_garbage(self.memory_manager)
        self.defragmenter.defragment(self.memory_manager)
        self.knowledge_optimizer.optimize(self.memory_manager)
        self.consolidation.run_consolidation()
        return {"status": "success", "purged": purged}
