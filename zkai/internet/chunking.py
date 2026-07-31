"""Web text chunking."""

from typing import List


class WebChunker:
    """Chunks web page text into semantic paragraphs for embedding and retrieval."""

    def __init__(self, chunk_size: int = 400):
        self.chunk_size = chunk_size

    def chunk(self, text: str) -> List[str]:
        words = text.split()
        chunks = []
        for i in range(0, len(words), self.chunk_size):
            chunks.append(" ".join(words[i : i + self.chunk_size]))
        return chunks
