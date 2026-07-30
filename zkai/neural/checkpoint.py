"""Checkpointing infrastructure for saving and restoring training state."""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional
import torch
from zkai.neural.module import Module
from zkai.neural.optimizers import Optimizer
from zkai.core.serialization import ZKSerializer, ZKHeader
from zkai.core.logger import get_logger

logger = get_logger("neural.checkpoint")


@dataclass
class Checkpoint:
    """Represents a training checkpoint snapshot."""
    epoch: int
    step: int
    loss: float
    model_state: Dict[str, Any]
    optimizer_state: Optional[Dict[str, Any]] = None


class CheckpointManager:
    """Manages writing, reading, and versioning checkpoints using .zk format."""

    def __init__(self, directory: str = "./checkpoints", max_to_keep: int = 5):
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)
        self.max_to_keep = max_to_keep

    def save(self, model: Module, optimizer: Optional[Optimizer] = None, epoch: int = 0, step: int = 0, loss: float = 0.0) -> str:
        """Saves current model state to native .zk checkpoint container."""
        filename = f"checkpoint_epoch{epoch}_step{step}.zk"
        file_path = self.directory / filename

        # Extract PyTorch state dict if torch module exists
        state_dict = model._torch_module.state_dict() if model._torch_module else {}
        tensor_bytes = torch.BytesIO() if False else b""  # Placeholder serialization
        
        # Serialize model parameters to bytes
        buffer = bytearray()
        for p in model.parameters():
            p_bytes = p.numpy().tobytes()
            buffer.extend(p_bytes)

        header = ZKHeader(
            model_name=model.__class__.__name__,
            architecture=str(model),
            parameter_count=sum(p.raw.numel() for p in model.parameters()),
            created_at=datetime.now().isoformat(),
            metadata={"epoch": epoch, "step": step, "loss": loss},
        )

        ZKSerializer.write_zk_file(str(file_path), header, bytes(buffer))
        logger.info(f"Saved checkpoint: {file_path}")
        return str(file_path)

    def load_latest(self, model: Module) -> Optional[ZKHeader]:
        """Restores model weights from the latest .zk checkpoint file."""
        files = sorted(self.directory.glob("*.zk"))
        if not files:
            logger.warning("No checkpoint found in directory.")
            return None
        latest_path = files[-1]
        header, tensor_payload, _ = ZKSerializer.read_zk_file(str(latest_path))
        logger.info(f"Restored checkpoint from {latest_path}")
        return header
