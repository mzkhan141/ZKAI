"""ZKAI Native Tensor Wrapper providing clean, framework-independent array operations."""

from typing import Any, List, Optional, Tuple, Union
import torch
from zkai.core.backend import BackendManager
from zkai.core.types import DType
from zkai.core.exceptions import NeuralError


class Tensor:
    """Native ZKAI Tensor class encapsulating backend compute operations."""

    def __init__(
        self,
        data: Any,
        dtype: Optional[DType] = None,
        device: Optional[str] = None,
        requires_grad: bool = False,
    ):
        backend = BackendManager.get_backend()
        if isinstance(data, torch.Tensor):
            self._tensor = data
            if requires_grad:
                self._tensor.requires_grad_(True)
        else:
            self._tensor = backend.tensor(data, dtype=dtype, device=device)
            if requires_grad:
                self._tensor.requires_grad_(True)

    @property
    def raw(self) -> torch.Tensor:
        """Returns the underlying PyTorch tensor for low-level backend computation."""
        return self._tensor

    @property
    def shape(self) -> Tuple[int, ...]:
        return tuple(self._tensor.shape)

    @property
    def dtype(self) -> str:
        return str(self._tensor.dtype)

    @property
    def device(self) -> str:
        return str(self._tensor.device)

    @property
    def grad(self) -> Optional["Tensor"]:
        if self._tensor.grad is not None:
            return Tensor(self._tensor.grad)
        return None

    @property
    def requires_grad(self) -> bool:
        return self._tensor.requires_grad

    def requires_grad_(self, requires: bool = True) -> "Tensor":
        self._tensor.requires_grad_(requires)
        return self

    def backward(self, gradient: Optional["Tensor"] = None) -> None:
        """Executes automatic differentiation / backward pass."""
        if gradient is not None:
            self._tensor.backward(gradient.raw)
        else:
            self._tensor.backward()

    def zero_grad(self) -> None:
        if self._tensor.grad is not None:
            self._tensor.grad.zero_()

    def numpy(self) -> Any:
        return self._tensor.detach().cpu().numpy()

    def item(self) -> Any:
        return self._tensor.item()

    def to(self, device: str) -> "Tensor":
        return Tensor(self._tensor.to(device))

    # --- Operator Overloads ---
    def __add__(self, other: Union["Tensor", float, int]) -> "Tensor":
        b = other.raw if isinstance(other, Tensor) else other
        return Tensor(self._tensor + b)

    def __sub__(self, other: Union["Tensor", float, int]) -> "Tensor":
        b = other.raw if isinstance(other, Tensor) else other
        return Tensor(self._tensor - b)

    def __mul__(self, other: Union["Tensor", float, int]) -> "Tensor":
        b = other.raw if isinstance(other, Tensor) else other
        return Tensor(self._tensor * b)

    def __truediv__(self, other: Union["Tensor", float, int]) -> "Tensor":
        b = other.raw if isinstance(other, Tensor) else other
        return Tensor(self._tensor / b)

    def __matmul__(self, other: "Tensor") -> "Tensor":
        return Tensor(torch.matmul(self._tensor, other.raw))

    def __repr__(self) -> str:
        return f"zkai.Tensor(shape={self.shape}, dtype={self._tensor.dtype}, device='{self.device}')"
