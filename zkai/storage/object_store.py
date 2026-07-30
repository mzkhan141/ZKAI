"""ObjectStore for storing and indexing structured JSON-serializable dict objects."""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from zkai.core.logger import get_logger

logger = get_logger("storage.object")


class ObjectStore:
    """Document/Object store persisting structured JSON objects."""

    def __init__(self, root_dir: Union[str, Path] = "./object_store"):
        self.root_dir = Path(root_dir)
        self.root_dir.mkdir(parents=True, exist_ok=True)
        self._index: Dict[str, Dict[str, Any]] = {}

    def put_object(self, object_id: str, obj: Dict[str, Any]) -> None:
        file_path = self.root_dir / f"{object_id}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(obj, f, indent=2)
        self._index[object_id] = obj

    def get_object(self, object_id: str) -> Optional[Dict[str, Any]]:
        if object_id in self._index:
            return self._index[object_id]
        file_path = self.root_dir / f"{object_id}.json"
        if not file_path.exists():
            return None
        with open(file_path, "r", encoding="utf-8") as f:
            obj = json.load(f)
            self._index[object_id] = obj
            return obj

    def delete_object(self, object_id: str) -> bool:
        if object_id in self._index:
            del self._index[object_id]
        file_path = self.root_dir / f"{object_id}.json"
        if file_path.exists():
            file_path.unlink()
            return True
        return False
