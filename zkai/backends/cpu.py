"""CPU compute backend implementation."""

from typing import Any, Optional, Tuple
import torch
from zkai.core.backend import PyTorchBackend
from zkai.core.types import DType


class CPUBackend(PyTorchBackend):
    """Explicit CPU compute backend."""

    def __init__(self):
        super().__init__(device="cpu")

    def name(self) -> str:
        return "CPUBackend"

    def is_available(self) -> bool:
        return True
