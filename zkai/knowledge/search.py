"""SemanticSearch engine across knowledge base."""

from typing import Any, List
from zkai.knowledge.indexer import EmbeddingIndexer


class SemanticSearch:
    """Executes dense vector similarity search across indexed KnowledgeBase documents."""

    def __init__(self, indexer: EmbeddingIndexer):
        self.indexer = indexer

    def search(self, query: str, top_k: int = 5) -> List[Any]:
        return self.indexer.vector_store.search(query, top_k=top_k)
