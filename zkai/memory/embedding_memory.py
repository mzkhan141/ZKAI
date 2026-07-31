"""EmbeddingMemory wrapping SentenceTransformers with native fallback."""

from typing import Any, List, Optional
import numpy as np
from zkai.memory.vector import VectorMemory
from zkai.memory.base import MemoryEntry
from zkai.core.logger import get_logger

logger = get_logger("memory.embedding")


class EmbeddingMemory(VectorMemory):
    """Dense Embedding Memory using SentenceTransformers or native vectorization fallback."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.encoder = None
        try:
            from sentence_transformers import SentenceTransformer
            self.encoder = SentenceTransformer(model_name)
            dim = self.encoder.get_sentence_embedding_dimension()
        except Exception as e:
            logger.debug(f"SentenceTransformers unavailable ({e}). Using native fallback encoder.")
            dim = 384
        super().__init__(dimension=dim)

    def _encode_text(self, text: str) -> List[float]:
        if self.encoder:
            return self.encoder.encode(text).tolist()
        # Native fallback vector encoding
        vec = np.zeros(self.dimension, dtype=np.float32)
        for i, char in enumerate(text):
            vec[i % self.dimension] += ord(char) / 255.0
        norm = np.linalg.norm(vec)
        return (vec / (norm if norm > 0 else 1.0)).tolist()

    def store_text(self, key: str, text: str, importance: float = 1.0) -> MemoryEntry:
        vec = self._encode_text(text)
        return self.store_vector(key, text, vec, importance=importance)

    def retrieve(self, query: str, top_k: int = 5) -> List[MemoryEntry]:
        query_vec = self._encode_text(query)
        return self.search_vector(query_vec, top_k=top_k)
