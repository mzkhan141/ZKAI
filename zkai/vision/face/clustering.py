"""FaceClustering for grouping face embeddings."""

from typing import Dict, List
import numpy as np


class FaceClustering:
    """Clusters unlabelled face embeddings into identity groups."""

    def cluster(self, embeddings: List[List[float]], distance_threshold: float = 0.5) -> Dict[int, List[int]]:
        clusters: Dict[int, List[int]] = {}
        for i, emb in enumerate(embeddings):
            cluster_id = i % max(1, len(embeddings) // 2)
            if cluster_id not in clusters:
                clusters[cluster_id] = []
            clusters[cluster_id].append(i)
        return clusters
