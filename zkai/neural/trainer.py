"""Trainer orchestrator for training neural networks and foundation architectures."""

from typing import Any, Iterable, Optional, Callable
import torch
from zkai.neural.module import Module
from zkai.neural.losses import Loss, MSELoss
from zkai.neural.optimizers import Optimizer, Adam
from zkai.neural.tensor import Tensor
from zkai.neural.checkpoint import CheckpointManager
from zkai.core.logger import get_logger

logger = get_logger("neural.trainer")


class Trainer:
    """High-level Training Loop Orchestrator for ZKAI neural models."""

    def __init__(
        self,
        model: Module,
        optimizer: Optional[Optimizer] = None,
        loss_fn: Optional[Loss] = None,
        checkpoint_dir: str = "./checkpoints",
    ):
        self.model = model
        self.optimizer = optimizer or Adam(self.model.parameters(), lr=1e-3)
        self.loss_fn = loss_fn or MSELoss()
        self.checkpoint_manager = CheckpointManager(directory=checkpoint_dir)

    def train_step(self, inputs: Tensor, targets: Tensor) -> float:
        """Executes a single forward pass, loss computation, backward pass, and optimizer step."""
        self.model.train()
        self.optimizer.zero_grad()
        outputs = self.model(inputs)
        loss = self.loss_fn(outputs, targets)
        loss.backward()
        self.optimizer.step()
        return float(loss.item())

    def fit(
        self,
        dataset: Iterable[tuple[Any, Any]],
        epochs: int = 5,
        val_dataset: Optional[Iterable[tuple[Any, Any]]] = None,
        callback: Optional[Callable[[int, float], None]] = None,
    ) -> float:
        """Fits the model on the provided dataset across epochs."""
        logger.info(f"Starting model training for {epochs} epochs...")
        last_loss = 0.0

        for epoch in range(1, epochs + 1):
            total_loss = 0.0
            count = 0
            for batch_x, batch_y in dataset:
                x_tensor = batch_x if isinstance(batch_x, Tensor) else Tensor(batch_x)
                y_tensor = batch_y if isinstance(batch_y, Tensor) else Tensor(batch_y)
                loss_val = self.train_step(x_tensor, y_tensor)
                total_loss += loss_val
                count += 1

            avg_loss = total_loss / max(1, count)
            last_loss = avg_loss
            logger.info(f"Epoch {epoch}/{epochs} - Loss: {avg_loss:.6f}")

            if callback:
                callback(epoch, avg_loss)

            self.checkpoint_manager.save(self.model, epoch=epoch, step=count, loss=avg_loss)

        logger.info("Training complete.")
        return last_loss
