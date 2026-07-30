"""TrainingHistory tracking metrics, best model state, and loss curves."""

from typing import Dict, List, Optional


class TrainingHistory:
    """Stores metrics history across epochs and tracks the best model epoch."""

    def __init__(self):
        self.epochs: List[int] = []
        self.metrics: Dict[str, List[float]] = {}
        self.best_epoch: Optional[int] = None
        self.best_loss: float = float("inf")

    def record_epoch(self, epoch: int, metrics: Dict[str, float]) -> None:
        self.epochs.append(epoch)
        for k, v in metrics.items():
            if k not in self.metrics:
                self.metrics[k] = []
            self.metrics[k].append(v)

        loss = metrics.get("val_loss", metrics.get("loss", float("inf")))
        if loss < self.best_loss:
            self.best_loss = loss
            self.best_epoch = epoch
