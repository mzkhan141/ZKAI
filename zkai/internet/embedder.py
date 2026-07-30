"""Web text Embedder with optional SentenceTransformer backend."""

from typing import List
import numpy as np

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None


class WebEmbedder:
    """Computes dense vector representations for web text snippets."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name) if SentenceTransformer else None

    def embed(self, texts: List[str]) -> List[List[float]]:
        if self.model:
            return self.model.encode(texts).tolist()
        results = []
        for text in texts:
            vec = np.zeros(384, dtype=np.float32)
            for i, ch in enumerate(text):
                vec[i % 384] += ord(ch) / 255.0
            norm = np.linalg.norm(vec)
            results.append((vec / (norm if norm > 0 else 1.0)).tolist())
        return results
