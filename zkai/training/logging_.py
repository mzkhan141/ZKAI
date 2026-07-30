"""Training metrics logging and TensorBoard integration."""

from typing import Dict, Any
from zkai.core.logger import get_logger

logger = get_logger("training.logger")


class TrainingLogger:
    """Logs training metrics, loss curves, and learning rates."""

    def log_metrics(self, step: int, loss: float, lr: float) -> None:
        logger.info(f"[Step {step}] Loss: {loss:.6f} | LR: {lr:.6e}")


class TensorBoardLogger:
    """TensorBoard logging integration."""

    def __init__(self, log_dir: str = "./tensorboard_logs"):
        self.log_dir = log_dir

    def add_scalar(self, tag: str, scalar_value: float, global_step: int) -> None:
        pass
