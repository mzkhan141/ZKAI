"""DocumentIndexer indexing chunks into vector indices for fast retrieval."""

from typing import List, Optional
from zkai.documents.document import DocumentChunk
from zkai.memory.vector import VectorMemory


class DocumentIndexer:
    """Indexes document chunks into a vector database for semantic search."""

    def __init__(self, vector_memory: Optional[VectorMemory] = None):
        self.vector_memory = vector_memory or VectorMemory()

    def index_chunks(self, chunks: List[DocumentChunk]) -> None:
        for chunk in chunks:
            if chunk.embedding is not None:
                self.vector_memory.store_vector(chunk.id, chunk.content, chunk.embedding)
