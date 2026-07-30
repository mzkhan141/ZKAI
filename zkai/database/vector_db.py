"""VectorDatabase wrapper around FAISS."""

from typing import List, Any
from zkai.memory.vector import VectorMemory


class VectorDatabase:
    """Vector Database layer for high-dimensional vector search."""

    def __init__(self, dimension: int = 384):
        self.memory = VectorMemory(dimension=dimension)

    def insert(self, key: str, content: str, vector: List[float]) -> None:
        self.memory.store_vector(key, content, vector)

    def search(self, query_vector: List[float], top_k: int = 5) -> List[Any]:
        return self.memory.search_vector(query_vector, top_k=top_k)
