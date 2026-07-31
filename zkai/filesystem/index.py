"""SemanticFileIndex and EmbeddingIndex for searching files by vector similarity."""

from typing import Dict, List, Optional
import torch
from zkai.embedding.index import SimilarityIndex
from zkai.embedding.text import TextEmbedding
from zkai.filesystem.files import SemanticFile
from zkai.core.logger import get_logger

logger = get_logger("filesystem.index")


class EmbeddingIndex:
    """Computes and maintains vector embeddings for SemanticFiles."""

    def __init__(self, dimension: int = 384):
        self.text_embedder = TextEmbedding(dimension=dimension)

    def embed_file(self, sem_file: SemanticFile, text_content: str) -> List[float]:
        vec_tensor = self.text_embedder.embed(text_content)
        raw_t = vec_tensor.raw if hasattr(vec_tensor, "raw") else vec_tensor
        vec_list = raw_t.squeeze(0).tolist() if hasattr(raw_t, "squeeze") else list(raw_t)
        sem_file.embedding_vector = vec_list
        return vec_list


class SemanticFileIndex:
    """Index organizing SemanticFiles by vector embeddings allowing semantic search."""

    def __init__(self, dimension: int = 384):
        self.similarity_index = SimilarityIndex(dimension=dimension)
        self.embedding_engine = EmbeddingIndex(dimension=dimension)
        self.file_map: Dict[int, SemanticFile] = {}
        self._next_id = 0

    def index_file(self, sem_file: SemanticFile, text_content: str) -> int:
        vec = self.embedding_engine.embed_file(sem_file, text_content)
        idx = self._next_id
        self._next_id += 1
        self.similarity_index.add(torch.tensor(vec), meta={"id": idx})
        self.file_map[idx] = sem_file
        logger.info(f"Indexed semantic file '{sem_file.name}' with ID {idx}")
        return idx

    def search(self, query: str, top_k: int = 5) -> List[SemanticFile]:
        query_vec = self.embedding_engine.text_embedder.embed(query)
        results = self.similarity_index.search(query_vec, top_k=top_k)
        matched_files = []
        for score, meta in results:
            doc_id = meta.get("id")
            if doc_id in self.file_map:
                matched_files.append(self.file_map[doc_id])
        return matched_files
