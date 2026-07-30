"""EmbeddingIndexer indexing KnowledgeBase entries into vector store."""

from typing import List
from zkai.knowledge.base import KnowledgeEntry
from zkai.memory.vector import VectorMemory


class EmbeddingIndexer:
    """Indexes KnowledgeBase text content into vector embeddings."""

    def __init__(self):
        self.vector_store = VectorMemory()

    def index_entry(self, entry: KnowledgeEntry) -> None:
        self.vector_store.store(entry.id, entry.content)
