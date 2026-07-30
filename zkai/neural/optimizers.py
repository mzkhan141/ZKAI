"""Optimization Algorithms (Adam, AdamW, SGD, RMSProp)."""

from typing import List, Iterable
import torch
import torch.optim as optim
from zkai.neural.parameter import Parameter


class Optimizer:
    """Base class for optimizers wrapping backend PyTorch optimizers."""

    def __init__(self, params: Iterable[Parameter], lr: float = 1e-3):
        self.params = list(params)
        self.lr = lr
        # Unwrap parameters to raw PyTorch tensors/parameters for optimization
        self._raw_params = [p.raw for p in self.params]
        self._optimizer: optim.Optimizer

    def step(self) -> None:
        """Performs a single optimization step."""
        if hasattr(self, "_optimizer"):
            self._optimizer.step()

    def zero_grad(self) -> None:
        """Clears the gradients of all optimized parameters."""
        if hasattr(self, "_optimizer"):
            self._optimizer.zero_grad()


class Adam(Optimizer):
    """Adam Optimizer."""

    def __init__(self, params: Iterable[Parameter], lr: float = 1e-3, betas: tuple[float, float] = (0.9, 0.999), eps: float = 1e-8, weight_decay: float = 0.0):
        super().__init__(params, lr)
        self._optimizer = optim.Adam(self._raw_params, lr=lr, betas=betas, eps=eps, weight_decay=weight_decay)

    def step(self) -> None:
        self._optimizer.step()


class AdamW(Optimizer):
    """AdamW Optimizer with decoupled weight decay."""

    def __init__(self, params: Iterable[Parameter], lr: float = 1e-3, betas: tuple[float, float] = (0.9, 0.999), eps: float = 1e-8, weight_decay: float = 0.01):
        super().__init__(params, lr)
        self._optimizer = optim.AdamW(self._raw_params, lr=lr, betas=betas, eps=eps, weight_decay=weight_decay)

    def step(self) -> None:
        self._optimizer.step()


class SGD(Optimizer):
    """Stochastic Gradient Descent Optimizer."""

    def __init__(self, params: Iterable[Parameter], lr: float = 1e-2, momentum: float = 0.0, weight_decay: float = 0.0):
        super().__init__(params, lr)
        self._optimizer = optim.SGD(self._raw_params, lr=lr, momentum=momentum, weight_decay=weight_decay)

    def step(self) -> None:
        self._optimizer.step()


class RMSProp(Optimizer):
    """RMSProp Optimizer."""

    def __init__(self, params: Iterable[Parameter], lr: float = 1e-2, alpha: float = 0.99, eps: float = 1e-8, weight_decay: float = 0.0, momentum: float = 0.0):
        super().__init__(params, lr)
        self._optimizer = optim.RMSprop(self._raw_params, lr=lr, alpha=alpha, eps=eps, weight_decay=weight_decay, momentum=momentum)

    def step(self) -> None:
        self._optimizer.step()
