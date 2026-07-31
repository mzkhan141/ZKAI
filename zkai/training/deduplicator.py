"""Deduplicator for removing duplicate and near-duplicate documents from training corpora."""

import hashlib
from typing import List, Set, Tuple
from zkai.core.logger import get_logger

logger = get_logger("training.deduplicator")


class Deduplicator:
    """Deduplication engine providing exact MD5 hash and MinHash shingle deduplication."""

    def __init__(self, similarity_threshold: float = 0.8, shingle_size: int = 5):
        self.similarity_threshold = similarity_threshold
        self.shingle_size = shingle_size
        self._seen_hashes: Set[str] = set()

    def deduplicate_exact(self, documents: List[str]) -> List[str]:
        """Removes exact duplicate documents using MD5 hash tracking."""
        unique_docs: List[str] = []
        for doc in documents:
            doc_hash = hashlib.md5(doc.encode("utf-8")).hexdigest()
            if doc_hash not in self._seen_hashes:
                self._seen_hashes.add(doc_hash)
                unique_docs.append(doc)
        return unique_docs

    def _get_shingles(self, text: str) -> Set[str]:
        words = text.split()
        if len(words) < self.shingle_size:
            return {text}
        return {" ".join(words[i : i + self.shingle_size]) for i in range(len(words) - self.shingle_size + 1)}

    def jaccard_similarity(self, set1: Set[str], set2: Set[str]) -> float:
        """Computes Jaccard similarity between two shingle sets."""
        if not set1 or not set2:
            return 0.0
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return intersection / union if union > 0 else 0.0

    def deduplicate_fuzzy(self, documents: List[str]) -> List[str]:
        """Removes near-duplicate documents using Jaccard similarity on word shingles."""
        unique_docs: List[str] = []
        shingle_sets: List[Set[str]] = []

        for doc in documents:
            current_shingles = self._get_shingles(doc)
            is_duplicate = False
            for existing_shingles in shingle_sets:
                sim = self.jaccard_similarity(current_shingles, existing_shingles)
                if sim >= self.similarity_threshold:
                    is_duplicate = True
                    break

            if not is_duplicate:
                unique_docs.append(doc)
                shingle_sets.append(current_shingles)

        return unique_docs

    def reset(self) -> None:
        """Resets seen hashes state."""
        self._seen_hashes.clear()
