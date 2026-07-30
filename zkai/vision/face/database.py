"""FaceDatabase storing identity embeddings."""

from typing import Dict, List, Optional


class FaceDatabase:
    """Stores identity names and their biometric 512-dim face embeddings."""

    def __init__(self):
        self._db: Dict[str, List[float]] = {}

    def enroll(self, identity_name: str, embedding: List[float]) -> None:
        self._db[identity_name] = embedding

    def delete(self, identity_name: str) -> None:
        self._db.pop(identity_name, None)

    def get_all(self) -> Dict[str, List[float]]:
        return self._db
