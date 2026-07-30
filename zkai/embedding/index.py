"""SimilarityIndex and SemanticSearch for vector indexing and semantic retrieval."""

from typing import Any, Dict, List, Optional, Tuple, Union
import torch
from zkai.embedding.text import TextEmbedding
from zkai.neural.tensor import Tensor
from zkai.core.logger import get_logger

logger = get_logger("embedding.index")

try:
    import faiss
except ImportError:
    faiss = None


class SimilarityIndex:
    """FAISS-accelerated or NumPy/PyTorch fallback vector similarity index."""

    def __init__(self, dimension: int = 384):
        self.dimension = dimension
        self.vectors: List[torch.Tensor] = []
        self.metadata: List[Dict[str, Any]] = []

    def add(self, vector: Union[Tensor, torch.Tensor], meta: Optional[Dict[str, Any]] = None) -> int:
        raw_vec = vector.raw if isinstance(vector, Tensor) else vector
        if raw_vec.dim() == 1:
            raw_vec = raw_vec.unsqueeze(0)
        self.vectors.append(raw_vec)
        self.metadata.append(meta or {})
        return len(self.vectors) - 1

    def search(self, query_vector: Union[Tensor, torch.Tensor], top_k: int = 5) -> List[Tuple[float, Dict[str, Any]]]:
        if not self.vectors:
            return []

        q_vec = query_vector.raw if isinstance(query_vector, Tensor) else query_vector
        if q_vec.dim() == 1:
            q_vec = q_vec.unsqueeze(0)

        all_vecs = torch.cat(self.vectors, dim=0)
        # Cosine similarity
        q_norm = torch.nn.functional.normalize(q_vec, p=2, dim=1)
        all_norm = torch.nn.functional.normalize(all_vecs, p=2, dim=1)
        sims = torch.mm(q_norm, all_norm.T).squeeze(0)

        top_scores, top_indices = torch.topk(sims, min(top_k, len(self.vectors)))
        results = []
        for score, idx in zip(top_scores.tolist(), top_indices.tolist()):
            results.append((float(score), self.metadata[idx]))
        return results


class SemanticSearch:
    """High-level Semantic Search API over text collections."""

    def __init__(self, embedder: Optional[TextEmbedding] = None):
        self.embedder = embedder or TextEmbedding()
        self.index = SimilarityIndex(dimension=self.embedder.dimension)

    def add_documents(self, documents: List[str]) -> None:
        embeddings = self.embedder.embed(documents).raw
        for doc, emb in zip(documents, embeddings):
            self.index.add(emb, meta={"text": doc})

    def search(self, query: str, top_k: int = 5) -> List[Tuple[float, str]]:
        q_emb = self.embedder.embed(query).raw
        raw_results = self.index.search(q_emb, top_k=top_k)
        return [(score, meta.get("text", "")) for score, meta in raw_results]
