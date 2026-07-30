"""Exponential Moving Average (EMA) of model weights."""

from typing import Dict
import torch
import torch.nn as nn
from zkai.neural.module import Module


class ExponentialMovingAverage:
    """Maintains moving average of model parameters for smoother inference weights."""

    def __init__(self, model: Module, decay: float = 0.999):
        self.model = model
        self.decay = decay
        self.shadow: Dict[str, torch.Tensor] = {}
        self.register()

    def register(self) -> None:
        for name, param in self.model._parameters.items():
            self.shadow[name] = param.raw.clone().detach()

    def update(self) -> None:
        for name, param in self.model._parameters.items():
            if name in self.shadow:
                new_average = (1.0 - self.decay) * param.raw.detach() + self.decay * self.shadow[name]
                self.shadow[name] = new_average.clone()
