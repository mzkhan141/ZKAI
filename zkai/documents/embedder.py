"""Document Embedder generating dense embeddings for document chunks."""

from typing import List
import numpy as np
from zkai.documents.document import Document, DocumentChunk

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None


class DocumentEmbedder:
    """Computes vector embeddings across document chunks."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name) if SentenceTransformer else None

    def _encode_text(self, text: str) -> List[float]:
        vec = np.zeros(384, dtype=np.float32)
        for i, char in enumerate(text):
            vec[i % 384] += ord(char) / 255.0
        norm = np.linalg.norm(vec)
        return (vec / (norm if norm > 0 else 1.0)).tolist()

    def embed_document(self, doc: Document) -> Document:
        """Encodes all chunks in a Document with dense vector embeddings."""
        if not doc.chunks:
            return doc
        texts = [chunk.content for chunk in doc.chunks]
        if self.model:
            embeddings = self.model.encode(texts).tolist()
        else:
            embeddings = [self._encode_text(t) for t in texts]

        for chunk, emb in zip(doc.chunks, embeddings):
            chunk.embedding = emb
        return doc
