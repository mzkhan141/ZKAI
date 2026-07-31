"""DocumentRetriever executing RAG semantic search over document chunks."""

from typing import List
import numpy as np
from zkai.memory.vector import VectorMemory
from zkai.memory.base import MemoryEntry

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None


class DocumentRetriever:
    """Retrieves relevant document chunks matching user queries."""

    def __init__(self, vector_memory: VectorMemory, model_name: str = "all-MiniLM-L6-v2"):
        self.vector_memory = vector_memory
        self.encoder = SentenceTransformer(model_name) if SentenceTransformer else None

    def _encode_query(self, query: str) -> List[float]:
        if self.encoder:
            return self.encoder.encode(query).tolist()
        vec = np.zeros(384, dtype=np.float32)
        for i, char in enumerate(query):
            vec[i % 384] += ord(char) / 255.0
        norm = np.linalg.norm(vec)
        return (vec / (norm if norm > 0 else 1.0)).tolist()

    def retrieve(self, query: str, top_k: int = 5) -> List[MemoryEntry]:
        query_vec = self._encode_query(query)
        return self.vector_memory.search_vector(query_vec, top_k=top_k)
