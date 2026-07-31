"""FaceIdentification 1:N database search."""

from typing import Dict, List, Optional, Tuple
import numpy as np


class FaceIdentification:
    """Searches query face embedding against identity database."""

    def identify(self, query_emb: list[float], database: Dict[str, list[float]], threshold: float = 0.6) -> Optional[Tuple[str, float]]:
        q_v = np.array(query_emb)
        best_match = None
        best_sim = -1.0
        for name, emb in database.items():
            db_v = np.array(emb)
            sim = float(np.dot(q_v, db_v) / (np.linalg.norm(q_v) * np.linalg.norm(db_v) + 1e-8))
            if sim > best_sim:
                best_sim = sim
                best_match = name
        if best_sim >= threshold:
            return best_match, best_sim
        return None
