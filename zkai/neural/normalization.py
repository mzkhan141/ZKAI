"""Normalization Layers (LayerNorm, BatchNorm, RMSNorm)."""

from typing import Union, Tuple
import torch
import torch.nn as nn
from zkai.neural.module import Module
from zkai.neural.tensor import Tensor


class LayerNorm(Module):
    """Layer Normalization layer."""

    def __init__(self, normalized_shape: Union[int, Tuple[int, ...]], eps: float = 1e-5):
        super().__init__()
        shape = (normalized_shape,) if isinstance(normalized_shape, int) else normalized_shape
        self._torch_module = nn.LayerNorm(shape, eps=eps)

    def forward(self, x: Tensor) -> Tensor:
        return Tensor(self._torch_module(x.raw))


class BatchNorm(Module):
    """Batch Normalization layer (1D/2D auto resolution)."""

    def __init__(self, num_features: int, eps: float = 1e-5, momentum: float = 0.1):
        super().__init__()
        self.num_features = num_features
        self._torch_module = nn.BatchNorm1d(num_features, eps=eps, momentum=momentum)

    def forward(self, x: Tensor) -> Tensor:
        if x.raw.dim() == 4:
            # 2D batchnorm fallback if spatial tensor
            bn2d = nn.BatchNorm2d(self.num_features, eps=self._torch_module.eps, device=x.raw.device)
            return Tensor(bn2d(x.raw))
        return Tensor(self._torch_module(x.raw))


class RMSNorm(Module):
    """Root Mean Square Layer Normalization (RMSNorm) popular in modern LLMs (LLaMA/Mistral)."""

    def __init__(self, hidden_dim: int, eps: float = 1e-6):
        super().__init__()
        self.eps = eps
        self.weight = nn.Parameter(torch.ones(hidden_dim))

    def forward(self, x: Tensor) -> Tensor:
        input_dtype = x.raw.dtype
        x_float = x.raw.to(torch.float32)
        variance = x_float.pow(2).mean(-1, keepdim=True)
        x_normed = x_float * torch.rsqrt(variance + self.eps)
        return Tensor((self.weight * x_normed).to(input_dtype))
