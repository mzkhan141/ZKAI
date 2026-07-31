"""StreamingDataset for infinite or large-scale dataset streams."""

from typing import Any, Callable, Generator, Iterable, Tuple
from zkai.datasets.base import Dataset


class StreamingDataset(Dataset):
    """Dataset streaming records lazily via generator function."""

    def __init__(self, generator_fn: Callable[[], Generator[Tuple[Any, Any], None, None]], estimated_length: int = 1000):
        self.generator_fn = generator_fn
        self.estimated_length = estimated_length

    def __len__(self) -> int:
        return self.estimated_length

    def __getitem__(self, idx: int) -> Tuple[Any, Any]:
        for i, item in enumerate(self.generator_fn()):
            if i == idx:
                return item
        raise IndexError(f"Index out of range for StreamingDataset: {idx}")

    def __iter__(self) -> Generator[Tuple[Any, Any], None, None]:
        yield from self.generator_fn()
