"""Base definitions and interfaces for Quantization subsystem."""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Tuple
import torch
from zkai.core.types import DType


class QuantizationMethod(str, Enum):
    DYNAMIC = "dynamic"
    STATIC = "static"
    WEIGHT_ONLY = "weight_only"


@dataclass
class QuantizationConfig:
    target_dtype: DType = DType.INT8
    method: QuantizationMethod = QuantizationMethod.WEIGHT_ONLY
    group_size: int = 128
    bits: int = 8
    symmetric: bool = True
