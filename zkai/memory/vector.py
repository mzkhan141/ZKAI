"""VectorMemory using FAISS index or native NumPy vector search for similarity retrieval."""

from typing import Any, List, Optional
import numpy as np
from zkai.memory.base import BaseMemory, MemoryEntry, MemoryMetadata
from zkai.core.types import MemoryType
from zkai.core.logger import get_logger

try:
    import faiss
except ImportError:
    faiss = None

logger = get_logger("memory.vector")


class VectorMemory(BaseMemory):
    """Vector Memory utilizing FAISS or native NumPy cosine similarity fallback."""

    def __init__(self, dimension: int = 384):
        super().__init__(MemoryType.VECTOR)
        self.dimension = dimension
        if faiss:
            self.index = faiss.IndexFlatIP(dimension)
        else:
            self.index = None
        self._entries: List[MemoryEntry] = []
        self._vectors: List[List[float]] = []

    def store_vector(self, key: str, content: Any, vector: List[float], importance: float = 1.0) -> MemoryEntry:
        vec_np = np.array([vector], dtype=np.float32)
        if faiss and self.index:
            faiss.normalize_L2(vec_np)
            self.index.add(vec_np)

        entry = MemoryEntry(
            key=key,
            content=content,
            memory_type=self.memory_type,
            metadata=MemoryMetadata(importance_score=importance),
            vector_embedding=vector,
        )
        self._entries.append(entry)
        self._vectors.append(vector)
        return entry

    def _text_to_vector(self, text: str) -> List[float]:
        import hashlib
        h = hashlib.sha256(text.encode("utf-8")).digest()
        raw_vals = [float(b) / 255.0 for b in h]
        repeated = (raw_vals * (self.dimension // len(raw_vals) + 1))[: self.dimension]
        return repeated

    def store(self, key: str, content: Any, importance: float = 1.0, tags: Optional[List[str]] = None) -> MemoryEntry:
        vec = self._text_to_vector(f"{key} {content}")
        return self.store_vector(key, content, vec, importance=importance)

    def search_vector(self, query_vector: List[float], top_k: int = 5) -> List[MemoryEntry]:
        if not self._entries:
            return []
        if faiss and self.index and self.index.ntotal > 0:
            q_np = np.array([query_vector], dtype=np.float32)
            faiss.normalize_L2(q_np)
            scores, indices = self.index.search(q_np, min(top_k, self.index.ntotal))
            results = []
            for idx in indices[0]:
                if 0 <= idx < len(self._entries):
                    results.append(self._entries[idx])
            return results

        # Native NumPy Cosine Similarity Fallback
        q_v = np.array(query_vector, dtype=np.float32)
        q_norm = np.linalg.norm(q_v)
        if q_norm == 0:
            q_norm = 1.0

        scores = []
        for i, vec in enumerate(self._vectors):
            v = np.array(vec, dtype=np.float32)
            v_norm = np.linalg.norm(v)
            sim = float(np.dot(q_v, v) / (q_norm * (v_norm if v_norm > 0 else 1.0)))
            scores.append((sim, i))

        scores.sort(key=lambda x: x[0], reverse=True)
        return [self._entries[idx] for _, idx in scores[:top_k]]

    def retrieve(self, query: str, top_k: int = 5) -> List[MemoryEntry]:
        query_vec = self._text_to_vector(query)
        return self.search_vector(query_vec, top_k=top_k)

    def clear(self) -> None:
        if faiss and self.index:
            self.index.reset()
        self._entries.clear()
        self._vectors.clear()
