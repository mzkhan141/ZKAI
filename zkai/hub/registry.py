"""CheckpointRegistry for versioned checkpoint tracking."""

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class CheckpointRecord:
    version: str
    file_path: str
    metrics: dict


class CheckpointRegistry:
    """Tracks versioned checkpoint artifacts across model families."""

    def __init__(self):
        self.records: Dict[str, List[CheckpointRecord]] = {}

    def register(self, model_name: str, record: CheckpointRecord) -> None:
        if model_name not in self.records:
            self.records[model_name] = []
        self.records[model_name].append(record)
