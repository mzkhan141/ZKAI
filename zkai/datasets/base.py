"""Base Dataset class with map, filter, select, and statistics."""

from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional, Tuple
from zkai.training.dataset import Dataset as BaseDataset


class Dataset(BaseDataset, ABC):
    """Enhanced Abstract Base Class for ZKAI Datasets."""

    def map(self, transform_fn: Callable[[Any], Any]) -> "MappedDataset":
        return MappedDataset(self, transform_fn)

    def filter(self, predicate_fn: Callable[[Any], bool]) -> "FilteredDataset":
        return FilteredDataset(self, predicate_fn)

    def select(self, indices: List[int]) -> "SubsetDataset":
        return SubsetDataset(self, indices)

    def statistics(self) -> Dict[str, Any]:
        return {"num_samples": len(self)}


class MappedDataset(Dataset):
    def __init__(self, dataset: Dataset, transform_fn: Callable[[Any], Any]):
        self.dataset = dataset
        self.transform_fn = transform_fn

    def __len__(self) -> int:
        return len(self.dataset)

    def __getitem__(self, idx: int) -> Any:
        item = self.dataset[idx]
        return self.transform_fn(item)


class FilteredDataset(Dataset):
    def __init__(self, dataset: Dataset, predicate_fn: Callable[[Any], bool]):
        self.dataset = dataset
        self.indices = [i for i in range(len(dataset)) if predicate_fn(dataset[i])]

    def __len__(self) -> int:
        return len(self.indices)

    def __getitem__(self, idx: int) -> Any:
        return self.dataset[self.indices[idx]]


class SubsetDataset(Dataset):
    def __init__(self, dataset: Dataset, indices: List[int]):
        self.dataset = dataset
        self.indices = indices

    def __len__(self) -> int:
        return len(self.indices)

    def __getitem__(self, idx: int) -> Any:
        return self.dataset[self.indices[idx]]
