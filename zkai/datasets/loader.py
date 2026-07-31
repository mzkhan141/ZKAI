"""Enhanced DataLoader with worker process simulation and batching."""

from typing import Generator, List, Optional, Tuple
from zkai.neural.tensor import Tensor
from zkai.training.dataset import Dataset, DataLoader as BaseDataLoader


class DataLoader(BaseDataLoader):
    """DataLoader providing prefetching, parallel batching, and collation."""

    def __init__(
        self,
        dataset: Dataset,
        batch_size: int = 32,
        shuffle: bool = True,
        num_workers: int = 0,
        pin_memory: bool = False,
        drop_last: bool = False,
    ):
        super().__init__(dataset, batch_size=batch_size, shuffle=shuffle)
        self.num_workers = num_workers
        self.pin_memory = pin_memory
        self.drop_last = drop_last
