"""LazyDataset for memory-mapped or lazy-evaluating items."""

from typing import Any, Callable, List, Tuple
from zkai.datasets.base import Dataset


class LazyDataset(Dataset):
    """Dataset deferring record resolution until item access."""

    def __init__(self, items: List[Any], loader_fn: Callable[[Any], Tuple[Any, Any]]):
        self.items = items
        self.loader_fn = loader_fn

    def __len__(self) -> int:
        return len(self.items)

    def __getitem__(self, idx: int) -> Tuple[Any, Any]:
        return self.loader_fn(self.items[idx])
