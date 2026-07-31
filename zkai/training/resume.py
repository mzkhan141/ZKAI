"""TrainingResumer for restoring training state and resuming execution."""

from typing import Optional
from zkai.neural.module import Module
from zkai.neural.checkpoint import CheckpointManager


class TrainingResumer:
    """Restores saved training state from disk and resumes training loop."""

    def __init__(self, checkpoint_dir: str = "./checkpoints"):
        self.manager = CheckpointManager(directory=checkpoint_dir)

    def resume_if_available(self, model: Module) -> Optional[int]:
        header = self.manager.load_latest(model)
        if header and "step" in header.metadata:
            return header.metadata["step"]
        return None
