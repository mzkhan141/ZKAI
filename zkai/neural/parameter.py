"""Parameter and Neuron primitives for neural models."""

from typing import Any, Optional
import torch
from zkai.neural.tensor import Tensor
from zkai.core.backend import BackendManager


class Parameter(Tensor):
    """Trainable model parameter wrapping backend Tensor with grad tracking enabled by default."""

    def __init__(self, data: Any, dtype: Optional[Any] = None, device: Optional[str] = None):
        super().__init__(data, dtype=dtype, device=device, requires_grad=True)
        # Register parameter as PyTorch nn.Parameter if needed
        self._param = torch.nn.Parameter(self._tensor)

    @property
    def raw_param(self) -> torch.nn.Parameter:
        return self._param


class Neuron:
    """Individual single artificial neuron primitive (Perceptron element)."""

    def __init__(self, input_dim: int = 1, activation: str = "sigmoid"):
        backend = BackendManager.get_backend()
        self.input_dim = input_dim
        self.weights = Parameter(backend.randn((input_dim, 1)))
        self.bias = Parameter(backend.zeros((1,)))
        self.activation = activation.lower()

    def forward(self, x: Tensor) -> Tensor:
        """Executes forward pass: act(w * x + b)."""
        z = (x @ self.weights) + self.bias
        if self.activation == "relu":
            return Tensor(torch.relu(z.raw))
        elif self.activation == "gelu":
            return Tensor(torch.nn.functional.gelu(z.raw))
        elif self.activation == "sigmoid":
            return Tensor(torch.sigmoid(z.raw))
        elif self.activation == "tanh":
            return Tensor(torch.tanh(z.raw))
        return z

    def __call__(self, x: Tensor) -> Tensor:
        return self.forward(x)

    def __repr__(self) -> str:
        return f"Neuron(input_dim={self.input_dim}, activation='{self.activation}')"
