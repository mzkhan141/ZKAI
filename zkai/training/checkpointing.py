"""Training Checkpoint state saving."""

from pathlib import Path
from zkai.neural.checkpoint import CheckpointManager


class TrainingCheckpoint:
    """Manages periodic checkpoint snapshots during training loops."""

    def __init__(self, checkpoint_dir: str = "./checkpoints"):
        self.manager = CheckpointManager(directory=checkpoint_dir)
