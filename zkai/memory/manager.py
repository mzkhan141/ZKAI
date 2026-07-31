"""MemoryManager orchestrating all 14 ZKAI memory subsystems."""

from typing import Any, List, Optional, Dict
from zkai.memory.base import MemoryEntry, BaseMemory
from zkai.memory.working import WorkingMemory
from zkai.memory.short_term import ShortTermMemory
from zkai.memory.long_term import LongTermMemory
from zkai.memory.episodic import EpisodicMemory
from zkai.memory.semantic import SemanticMemory
from zkai.memory.procedural import ProceduralMemory
from zkai.memory.entity import EntityMemory
from zkai.memory.knowledge_graph import KnowledgeGraph
from zkai.memory.vector import VectorMemory
from zkai.memory.file_memory import FileMemory
from zkai.memory.code_memory import CodeMemory
from zkai.memory.retrieval import MemoryRetriever
from zkai.memory.consolidation import MemoryConsolidator
from zkai.core.logger import get_logger

logger = get_logger("memory.manager")


class MemoryManager:
    """Master Memory Subsystem Manager for ZKAI AI Operating System."""

    def __init__(self, persistence_dir: str = "./memory_store"):
        self.working = WorkingMemory()
        self.short_term = ShortTermMemory()
        self.long_term = LongTermMemory(storage_dir=persistence_dir)
        self.episodic = EpisodicMemory()
        self.semantic = SemanticMemory()
        self.procedural = ProceduralMemory()
        self.entity = EntityMemory()
        self.knowledge_graph = KnowledgeGraph()
        self.vector = VectorMemory()
        self.file = FileMemory()
        self.code = CodeMemory()

        self.retriever = MemoryRetriever([
            self.working,
            self.short_term,
            self.long_term,
            self.episodic,
            self.semantic,
            self.vector,
            self.file,
            self.code,
        ])
        self.consolidator = MemoryConsolidator()

    def remember(self, text_or_key: str, content: Any = None, importance: float = 1.0) -> MemoryEntry:
        """Stores a new memory into short-term and long-term memory."""
        val = content if content is not None else text_or_key
        self.working.store(text_or_key, val, importance=importance)
        self.short_term.store(text_or_key, val, importance=importance)
        return self.long_term.store(text_or_key, val, importance=importance)

    def search(self, query: str, top_k: int = 5) -> List[MemoryEntry]:
        """Searches across all memory subsystems using unified retrieval."""
        return self.retriever.search(query, top_k=top_k)

    def consolidate(self) -> None:
        """Triggers memory consolidation and decay purging."""
        keep, purge = self.consolidator.consolidate(list(self.short_term._store.values()))
        for entry in keep:
            self.long_term.store(entry.key, entry.content, importance=entry.metadata.importance_score)
