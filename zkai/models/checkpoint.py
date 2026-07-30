"""Model Checkpoint and Versioning Management."""

from pathlib import Path
from typing import Dict, List, Optional
from zkai.core.logger import get_logger

logger = get_logger("models.checkpoint")


class VersionManager:
    """Manages semantic version strings and tag assignments for model weights."""

    @staticmethod
    def bump_version(current: str, release_type: str = "patch") -> str:
        parts = [int(p) for p in current.split(".")]
        if release_type == "major":
            parts[0] += 1
            parts[1] = 0
            parts[2] = 0
        elif release_type == "minor":
            parts[1] += 1
            parts[2] = 0
        else:
            parts[2] += 1
        return ".".join(str(p) for p in parts)


class ModelCheckpointManager:
    """High-level Model Checkpoint Orchestrator."""

    def __init__(self, base_dir: str = "./model_checkpoints"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.version_manager = VersionManager()

    def list_checkpoints(self) -> List[str]:
        return [str(p) for p in self.base_dir.glob("*.zk")]
