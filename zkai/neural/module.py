"""Base Module, Sequential, NeuralNetwork, and Model abstractions."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
import torch
import torch.nn as nn
from zkai.neural.tensor import Tensor
from zkai.neural.parameter import Parameter
from zkai.core.backend import BackendManager
from zkai.core.logger import get_logger

logger = get_logger("neural.module")


class Module(ABC):
    """Abstract Base Class for all ZKAI neural modules and network layers."""

    def __init__(self):
        self._backend = BackendManager.get_backend()
        self._submodules: Dict[str, "Module"] = {}
        self._parameters: Dict[str, Parameter] = {}
        self._training: bool = True
        self._torch_module: Optional[nn.Module] = None

    @property
    def training(self) -> bool:
        return self._training

    def train(self, mode: bool = True) -> "Module":
        """Sets module training state."""
        self._training = mode
        if self._torch_module:
            self._torch_module.train(mode)
        for sub in self._submodules.values():
            sub.train(mode)
        return self

    def eval(self) -> "Module":
        """Sets module evaluation state."""
        return self.train(False)

    @abstractmethod
    def forward(self, *args: Any, **kwargs: Any) -> Any:
        """Executes forward computation."""
        pass

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self.forward(*args, **kwargs)

    def parameters(self) -> List[Parameter]:
        """Returns list of trainable parameters in this module and submodules."""
        params: List[Parameter] = list(self._parameters.values())
        if self._torch_module:
            for p in self._torch_module.parameters():
                params.append(Parameter(p))
        for sub in self._submodules.values():
            params.extend(sub.parameters())
        return params

    def to(self, device: str) -> "Module":
        """Moves module parameters to specified device."""
        if self._torch_module:
            self._torch_module.to(device)
        for sub in self._submodules.values():
            sub.to(device)
        return self

    def zero_grad(self) -> None:
        """Zeros out gradients of all parameters."""
        for p in self.parameters():
            p.zero_grad()


class Sequential(Module):
    """Sequential container executing modules in sequence order."""

    def __init__(self, *args: Module):
        super().__init__()
        self.layers: List[Module] = list(args)
        for idx, module in enumerate(self.layers):
            self._submodules[f"layer_{idx}"] = module

    def forward(self, input_tensor: Tensor) -> Tensor:
        current = input_tensor
        for layer in self.layers:
            current = layer(current)
        return current


class NeuralNetwork(Module):
    """NeuralNetwork wrapper class representing an assembled multi-layer network."""

    def __init__(self, layers: Optional[List[Module]] = None):
        super().__init__()
        self.sequential = Sequential(*layers) if layers else Sequential()
        self._submodules["sequential"] = self.sequential

    def add_layer(self, layer: Module) -> None:
        self.sequential.layers.append(layer)
        self.sequential._submodules[f"layer_{len(self.sequential.layers)-1}"] = layer

    def forward(self, x: Tensor) -> Tensor:
        return self.sequential(x)


class Model(NeuralNetwork):
    """Base model wrapper providing save, load, and summary interfaces."""

    def summary(self) -> str:
        param_count = sum(p.raw.numel() for p in self.parameters())
        return f"{self.__class__.__name__} | Parameters: {param_count:,}"
