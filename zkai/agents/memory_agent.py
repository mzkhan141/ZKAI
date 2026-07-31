"""MemoryAgent specialized in knowledge recall and store."""

from zkai.memory.manager import MemoryManager


class MemoryAgent:
    """Specialized Agent for memory retrieval, consolidation, and indexing."""

    def __init__(self):
        self.memory = MemoryManager()

    def store_knowledge(self, key: str, value: str) -> None:
        self.memory.remember(key, value)
