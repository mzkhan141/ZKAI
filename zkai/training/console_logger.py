"""ConsoleLogger for formatted terminal output."""

from typing import Dict
from zkai.core.logger import get_logger

logger = get_logger("training.console")


class ConsoleLogger:
    """Formats training progress and metric outputs to console log."""

    def log_epoch(self, epoch: int, total_epochs: int, metrics: Dict[str, float]) -> None:
        metrics_str = " | ".join(f"{k}: {v:.6f}" for k, v in metrics.items())
        logger.info(f"Epoch [{epoch}/{total_epochs}] -> {metrics_str}")
