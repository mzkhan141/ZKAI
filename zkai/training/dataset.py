"""Dataset, DataLoader, and DataPipeline for tokenization, cleaning, streaming, and batching."""

from abc import ABC, abstractmethod
from typing import Any, Generator, Iterable, List, Optional, Tuple
import torch
from torch.utils.data import Dataset as PyTorchDataset, DataLoader as PyTorchDataLoader
from zkai.neural.tensor import Tensor


class Dataset(ABC):
    """Abstract Base Class for ZKAI Datasets."""

    @abstractmethod
    def __len__(self) -> int:
        pass

    @abstractmethod
    def __getitem__(self, idx: int) -> Tuple[Any, Any]:
        pass


class SimpleDataset(Dataset):
    """Simple in-memory Dataset container."""

    def __init__(self, inputs: List[Any], targets: List[Any]):
        self.inputs = inputs
        self.targets = targets

    def __len__(self) -> int:
        return len(self.inputs)

    def __getitem__(self, idx: int) -> Tuple[Any, Any]:
        return self.inputs[idx], self.targets[idx]


class DataLoader:
    """Batch data loader providing shuffling, streaming, and batch generation."""

    def __init__(self, dataset: Dataset, batch_size: int = 32, shuffle: bool = True):
        self.dataset = dataset
        self.batch_size = batch_size
        self.shuffle = shuffle

    def __len__(self) -> int:
        import math
        return math.ceil(len(self.dataset) / self.batch_size)

    def __iter__(self) -> Generator[Tuple[Tensor, Tensor], None, None]:
        indices = list(range(len(self.dataset)))
        if self.shuffle:
            import random
            random.shuffle(indices)

        for i in range(0, len(indices), self.batch_size):
            batch_idx = indices[i : i + self.batch_size]
            batch_x = [self.dataset[j][0] for j in batch_idx]
            batch_y = [self.dataset[j][1] for j in batch_idx]
            yield Tensor(batch_x), Tensor(batch_y)


class DataPipeline:
    """Pre-processing pipeline for cleaning, deduplicating, and tokenizing raw datasets."""

    def clean_text(self, text: str) -> str:
        return " ".join(text.split())
