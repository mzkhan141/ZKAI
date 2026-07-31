"""Collators for batch preparation, padding, and dynamic batching."""

from typing import Any, Dict, List, Tuple
import torch
from zkai.neural.tensor import Tensor


class Collator:
    """Combines individual items into a batched Tensor structure."""

    def __call__(self, batch: List[Tuple[Any, Any]]) -> Tuple[Tensor, Tensor]:
        xs = [item[0] for item in batch]
        ys = [item[1] for item in batch]
        return Tensor(xs), Tensor(ys)


class PaddingCollator(Collator):
    """Pads variable length sequence elements in batch to max sequence length."""

    def __init__(self, pad_value: int = 0):
        self.pad_value = pad_value

    def __call__(self, batch: List[Tuple[List[int], List[int]]]) -> Tuple[Tensor, Tensor]:
        max_x = max(len(item[0]) if isinstance(item[0], list) else 1 for item in batch)
        padded_x = []
        padded_y = []
        for x, y in batch:
            if isinstance(x, list):
                px = x + [self.pad_value] * (max_x - len(x))
            else:
                px = x
            padded_x.append(px)
            padded_y.append(y)
        return Tensor(padded_x), Tensor(padded_y)
