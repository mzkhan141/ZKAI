"""BlobStore for storing and retrieving raw binary payloads on filesystem."""

import hashlib
import os
from pathlib import Path
from typing import Optional, Union
from zkai.core.logger import get_logger

logger = get_logger("storage.blob")


class BlobStore:
    """Binary Large Object (BLOB) store organizing files by content addressable hash."""

    def __init__(self, root_dir: Union[str, Path] = "./blob_store"):
        self.root_dir = Path(root_dir)
        self.root_dir.mkdir(parents=True, exist_ok=True)

    def put(self, data: bytes) -> str:
        """Stores binary payload and returns SHA256 content key."""
        blob_key = hashlib.sha256(data).hexdigest()
        file_path = self.root_dir / blob_key[:2] / blob_key
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(data)
        return blob_key

    def get(self, blob_key: str) -> Optional[bytes]:
        """Retrieves binary payload for given SHA256 key."""
        file_path = self.root_dir / blob_key[:2] / blob_key
        if not file_path.exists():
            return None
        with open(file_path, "rb") as f:
            return f.read()

    def delete(self, blob_key: str) -> bool:
        """Removes stored blob payload."""
        file_path = self.root_dir / blob_key[:2] / blob_key
        if file_path.exists():
            os.remove(file_path)
            return True
        return False
