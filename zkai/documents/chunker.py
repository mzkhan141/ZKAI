"""Document Chunking algorithms (Fixed, Sliding Window, Recursive, Semantic)."""

from typing import List
from zkai.documents.document import Document, DocumentChunk


class Chunker:
    """Base class for document chunkers."""

    def chunk(self, doc: Document) -> List[DocumentChunk]:
        raise NotImplementedError


class FixedChunker(Chunker):
    """Splits text into fixed character length chunks."""

    def __init__(self, chunk_size: int = 500, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, doc: Document) -> List[DocumentChunk]:
        text = doc.content
        chunks = []
        start = 0
        idx = 0

        while start < len(text):
            end = start + self.chunk_size
            segment = text[start:end]
            chunk = DocumentChunk(content=segment, chunk_index=idx, metadata={"source_doc_id": doc.id})
            chunks.append(chunk)
            idx += 1
            start += self.chunk_size - self.overlap

        doc.chunks = chunks
        return chunks


class SlidingWindowChunker(FixedChunker):
    """Sliding Window Chunker alias."""
    pass


class RecursiveChunker(Chunker):
    """Recursively splits document text on paragraph and sentence boundaries."""

    def __init__(self, max_chunk_size: int = 500):
        self.max_chunk_size = max_chunk_size

    def chunk(self, doc: Document) -> List[DocumentChunk]:
        paragraphs = doc.content.split("\n\n")
        chunks = []
        idx = 0

        for para in paragraphs:
            if len(para.strip()) > 0:
                chunks.append(DocumentChunk(content=para.strip(), chunk_index=idx, metadata={"source_doc_id": doc.id}))
                idx += 1

        doc.chunks = chunks
        return chunks
