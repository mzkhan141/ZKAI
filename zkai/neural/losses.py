"""Loss Functions (CrossEntropy, MSE, ContrastiveLoss)."""

from abc import ABC, abstractmethod
import torch
import torch.nn as nn
from zkai.neural.module import Module
from zkai.neural.tensor import Tensor


class Loss(Module, ABC):
    """Abstract Base Class for loss functions."""

    @abstractmethod
    def forward(self, predictions: Tensor, targets: Tensor) -> Tensor:
        pass


class CrossEntropyLoss(Loss):
    """Cross Entropy Loss for classification and token prediction."""

    def __init__(self, ignore_index: int = -100):
        super().__init__()
        self._torch_module = nn.CrossEntropyLoss(ignore_index=ignore_index)

    def forward(self, predictions: Tensor, targets: Tensor) -> Tensor:
        preds = predictions.raw
        targs = targets.raw
        if preds.dim() == 3:  # (batch, seq_len, vocab) -> reshape for token CE
            preds = preds.view(-1, preds.size(-1))
            targs = targs.view(-1)
        return Tensor(self._torch_module(preds, targs.long()))


class CrossEntropy(CrossEntropyLoss):
    """Alias for CrossEntropyLoss."""
    pass


class MSELoss(Loss):
    """Mean Squared Error Loss."""

    def __init__(self):
        super().__init__()
        self._torch_module = nn.MSELoss()

    def forward(self, predictions: Tensor, targets: Tensor) -> Tensor:
        return Tensor(self._torch_module(predictions.raw, targets.raw))


class MSE(MSELoss):
    """Alias for MSELoss."""
    pass


class ContrastiveLoss(Loss):
    """Contrastive loss for representation learning and embeddings."""

    def __init__(self, margin: float = 1.0):
        super().__init__()
        self.margin = margin

    def forward(self, predictions: Tensor, targets: Tensor) -> Tensor:
        # Distance calculation
        euclidean_distance = nn.functional.pairwise_distance(predictions.raw, targets.raw)
        loss = torch.mean((1 - targets.raw) * torch.pow(euclidean_distance, 2) +
                          (targets.raw) * torch.pow(torch.clamp(self.margin - euclidean_distance, min=0.0), 2))
        return Tensor(loss)
