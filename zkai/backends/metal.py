"""Metal compute backend for Apple Silicon."""

import torch
from zkai.core.backend import PyTorchBackend


class MetalBackend(PyTorchBackend):
    """Apple Metal Performance Shaders (MPS) compute backend."""

    def __init__(self):
        device_str = "mps" if hasattr(torch.backends, "mps") and torch.backends.mps.is_available() else "cpu"
        super().__init__(device=device_str)

    def name(self) -> str:
        return "MetalBackend"

    def is_available(self) -> bool:
        return hasattr(torch.backends, "mps") and torch.backends.mps.is_available()
