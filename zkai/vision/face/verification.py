"""FaceVerification 1:1 similarity matching."""

import numpy as np


class FaceVerification:
    """Verifies whether two 512-dim face embeddings belong to the same identity."""

    @staticmethod
    def verify(emb1: list[float], emb2: list[float], threshold: float = 0.6) -> bool:
        v1 = np.array(emb1)
        v2 = np.array(emb2)
        similarity = float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-8))
        return similarity >= threshold
