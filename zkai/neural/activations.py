"""Activation functions (ReLU, GELU, SiLU, Sigmoid, Softmax, Swish)."""

import torch
import torch.nn as nn
from zkai.neural.module import Module
from zkai.neural.tensor import Tensor


class Activation(Module):
    """Base class for all activation layers."""
    pass


class ReLU(Activation):
    """Rectified Linear Unit Activation."""

    def __init__(self, inplace: bool = False):
        super().__init__()
        self._torch_module = nn.ReLU(inplace=inplace)

    def forward(self, x: Tensor) -> Tensor:
        return Tensor(self._torch_module(x.raw))


class GELU(Activation):
    """Gaussian Error Linear Unit Activation."""

    def __init__(self, approximate: str = "none"):
        super().__init__()
        self._torch_module = nn.GELU(approximate=approximate)

    def forward(self, x: Tensor) -> Tensor:
        return Tensor(self._torch_module(x.raw))


class SiLU(Activation):
    """Sigmoid Linear Unit (Swish) Activation."""

    def __init__(self):
        super().__init__()
        self._torch_module = nn.SiLU()

    def forward(self, x: Tensor) -> Tensor:
        return Tensor(self._torch_module(x.raw))


class Swish(SiLU):
    """Swish activation alias for SiLU."""
    pass


class Sigmoid(Activation):
    """Sigmoid Activation."""

    def __init__(self):
        super().__init__()
        self._torch_module = nn.Sigmoid()

    def forward(self, x: Tensor) -> Tensor:
        return Tensor(self._torch_module(x.raw))


class Softmax(Activation):
    """Softmax Activation."""

    def __init__(self, dim: int = -1):
        super().__init__()
        self.dim = dim
        self._torch_module = nn.Softmax(dim=dim)

    def forward(self, x: Tensor) -> Tensor:
        return Tensor(self._torch_module(x.raw))
