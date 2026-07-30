"""Neural Layer Primitives (Dense, Linear, Conv1D/2D/3D, Embedding, Dropout)."""

from typing import Optional, Union, Tuple
import torch
import torch.nn as nn
from zkai.neural.module import Module
from zkai.neural.tensor import Tensor


class Linear(Module):
    """Fully Connected Linear Layer."""

    def __init__(self, in_features: int, out_features: int, bias: bool = True):
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features
        self._torch_module = nn.Linear(in_features, out_features, bias=bias)

    def forward(self, x: Tensor) -> Tensor:
        return Tensor(self._torch_module(x.raw))


class Dense(Linear):
    """Dense Layer alias for Linear Layer."""
    pass


class Conv1D(Module):
    """1D Convolutional Layer for sequential and temporal data."""

    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        kernel_size: int,
        stride: int = 1,
        padding: int = 0,
        dilation: int = 1,
        groups: int = 1,
        bias: bool = True,
    ):
        super().__init__()
        self._torch_module = nn.Conv1d(
            in_channels,
            out_channels,
            kernel_size,
            stride=stride,
            padding=padding,
            dilation=dilation,
            groups=groups,
            bias=bias,
        )

    def forward(self, x: Tensor) -> Tensor:
        return Tensor(self._torch_module(x.raw))


class Conv2D(Module):
    """2D Convolutional Layer for spatial image processing."""

    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        kernel_size: Union[int, Tuple[int, int]],
        stride: Union[int, Tuple[int, int]] = 1,
        padding: Union[int, Tuple[int, int]] = 0,
        bias: bool = True,
    ):
        super().__init__()
        self._torch_module = nn.Conv2d(
            in_channels, out_channels, kernel_size, stride=stride, padding=padding, bias=bias
        )

    def forward(self, x: Tensor) -> Tensor:
        return Tensor(self._torch_module(x.raw))


class Conv3D(Module):
    """3D Convolutional Layer for volumetric or video frame processing."""

    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        kernel_size: Union[int, Tuple[int, int, int]],
        stride: Union[int, Tuple[int, int, int]] = 1,
        padding: Union[int, Tuple[int, int, int]] = 0,
        bias: bool = True,
    ):
        super().__init__()
        self._torch_module = nn.Conv3d(
            in_channels, out_channels, kernel_size, stride=stride, padding=padding, bias=bias
        )

    def forward(self, x: Tensor) -> Tensor:
        return Tensor(self._torch_module(x.raw))


class Embedding(Module):
    """Lookup table embedding layer mapping token indices to dense vectors."""

    def __init__(self, num_embeddings: int, embedding_dim: int, padding_idx: Optional[int] = None):
        super().__init__()
        self.num_embeddings = num_embeddings
        self.embedding_dim = embedding_dim
        self._torch_module = nn.Embedding(num_embeddings, embedding_dim, padding_idx=padding_idx)

    def forward(self, x: Tensor) -> Tensor:
        return Tensor(self._torch_module(x.raw.long()))


class Dropout(Module):
    """Dropout regularization layer."""

    def __init__(self, p: float = 0.5):
        super().__init__()
        self.p = p
        self._torch_module = nn.Dropout(p=p)

    def forward(self, x: Tensor) -> Tensor:
        return Tensor(self._torch_module(x.raw))
