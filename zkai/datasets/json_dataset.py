"""JSONDataset for JSON and JSONL datasets."""

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple
from zkai.datasets.base import Dataset


class JSONDataset(Dataset):
    """Dataset reading JSON and JSONL records."""

    def __init__(self, file_path: str):
        self.path = Path(file_path)
        self.data: List[Any] = []
        if self.path.suffix == ".jsonl":
            lines = self.path.read_text(encoding="utf-8").splitlines()
            self.data = [json.loads(line) for line in lines if line.strip()]
        else:
            content = json.loads(self.path.read_text(encoding="utf-8"))
            self.data = content if isinstance(content, list) else [content]

    def __len__(self) -> int:
        return len(self.data)

    def __getitem__(self, idx: int) -> Tuple[Any, Any]:
        item = self.data[idx]
        if isinstance(item, dict):
            inp = item.get("input", item.get("text", str(item)))
            tgt = item.get("output", item.get("label", inp))
            return inp, tgt
        return item, item
