"""TextEmbedding generator using sentence-transformers or native hash vectors."""

from typing import Any, List, Union
import torch
from zkai.embedding.model import EmbeddingModel
from zkai.neural.tensor import Tensor
from zkai.core.types import EmbeddingModalityType

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None


class TextEmbedding(EmbeddingModel):
    """Text embedding generator."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2", dimension: int = 384):
        super().__init__(dimension=dimension, modality=EmbeddingModalityType.TEXT)
        self.st_model = SentenceTransformer(model_name) if SentenceTransformer else None

    def embed(self, inputs: Union[str, List[str]]) -> Tensor:
        texts = [inputs] if isinstance(inputs, str) else list(inputs)
        if self.st_model:
            embeddings = self.st_model.encode(texts, convert_to_tensor=True)
            return Tensor(embeddings)
        else:
            # Fallback deterministic pseudo-embedding
            batch_vecs = []
            for t in texts:
                vec = [float(ord(c) % 100) / 100.0 for c in (t * 50)[: self.dimension]]
                if len(vec) < self.dimension:
                    vec.extend([0.0] * (self.dimension - len(vec)))
                batch_vecs.append(vec)
            return Tensor(torch.tensor(batch_vecs))
