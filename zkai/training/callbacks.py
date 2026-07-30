"""TrainerCallbacks lifecycle system."""

from abc import ABC
from typing import Any, List


class TrainerCallback(ABC):
    def on_train_begin(self, logs: Any = None) -> None:
        pass

    def on_train_end(self, logs: Any = None) -> None:
        pass

    def on_epoch_begin(self, epoch: int, logs: Any = None) -> None:
        pass

    def on_epoch_end(self, epoch: int, logs: Any = None) -> None:
        pass

    def on_batch_begin(self, batch: int, logs: Any = None) -> None:
        pass

    def on_batch_end(self, batch: int, logs: Any = None) -> None:
        pass


class CallbackList:
    """Manages collection of TrainerCallbacks."""

    def __init__(self, callbacks: List[TrainerCallback]):
        self.callbacks = callbacks

    def on_epoch_end(self, epoch: int, logs: Any = None) -> None:
        for cb in self.callbacks:
            cb.on_epoch_end(epoch, logs)

    def on_batch_end(self, batch: int, logs: Any = None) -> None:
        for cb in self.callbacks:
            cb.on_batch_end(batch, logs)
