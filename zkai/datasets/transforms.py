"""Transforms and Compose pipeline for data augmentations."""

from abc import ABC, abstractmethod
from typing import Any, List


class Transform(ABC):
    @abstractmethod
    def __call__(self, sample: Any) -> Any:
        pass


class Compose(Transform):
    """Chains multiple data transforms in sequence."""

    def __init__(self, transforms: List[Transform]):
        self.transforms = transforms

    def __call__(self, sample: Any) -> Any:
        current = sample
        for t in self.transforms:
            current = t(current)
        return current


class Normalize(Transform):
    def __init__(self, mean: float = 0.0, std: float = 1.0):
        self.mean = mean
        self.std = std

    def __call__(self, sample: Any) -> Any:
        return sample
