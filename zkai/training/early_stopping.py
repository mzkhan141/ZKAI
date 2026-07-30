"""EarlyStopping callback for training loop termination."""

from typing import Optional
from zkai.core.logger import get_logger

logger = get_logger("training.early_stopping")


class EarlyStopping:
    """Terminates training when validation loss stops improving."""

    def __init__(self, patience: int = 5, min_delta: float = 1e-4):
        self.patience = patience
        self.min_delta = min_delta
        self.best_loss = float("inf")
        self.counter = 0
        self.should_stop = False

    def check(self, val_loss: float) -> bool:
        if val_loss < self.best_loss - self.min_delta:
            self.best_loss = val_loss
            self.counter = 0
        else:
            self.counter += 1
            if self.counter >= self.patience:
                self.should_stop = True
                logger.info(f"EarlyStopping triggered after {self.counter} unimproved epochs.")
        return self.should_stop
