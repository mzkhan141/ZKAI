"""Samplers for dataset iteration: Random, Sequential, Distributed, Weighted, Batch."""

from abc import ABC, abstractmethod
import random
from typing import Iterator, List, Sequence, Union


class Sampler(ABC):
    @abstractmethod
    def __iter__(self) -> Iterator[int]:
        pass

    @abstractmethod
    def __len__(self) -> int:
        pass


class SequentialSampler(Sampler):
    def __init__(self, data_source: Sequence):
        self.data_source = data_source

    def __iter__(self) -> Iterator[int]:
        return iter(range(len(self.data_source)))

    def __len__(self) -> int:
        return len(self.data_source)


class RandomSampler(Sampler):
    def __init__(self, data_source: Sequence):
        self.data_source = data_source

    def __iter__(self) -> Iterator[int]:
        indices = list(range(len(self.data_source)))
        random.shuffle(indices)
        return iter(indices)

    def __len__(self) -> int:
        return len(self.data_source)


class DistributedSampler(Sampler):
    def __init__(self, data_source: Sequence, num_replicas: int = 1, rank: int = 0):
        self.data_source = data_source
        self.num_replicas = num_replicas
        self.rank = rank
        self.indices = list(range(len(data_source)))[rank::num_replicas]

    def __iter__(self) -> Iterator[int]:
        return iter(self.indices)

    def __len__(self) -> int:
        return len(self.indices)


class WeightedSampler(Sampler):
    def __init__(self, weights: List[float], num_samples: int):
        self.weights = weights
        self.num_samples = num_samples

    def __iter__(self) -> Iterator[int]:
        choices = random.choices(range(len(self.weights)), weights=self.weights, k=self.num_samples)
        return iter(choices)

    def __len__(self) -> int:
        return self.num_samples


class BatchSampler(Sampler):
    def __init__(self, sampler: Sampler, batch_size: int, drop_last: bool = False):
        self.sampler = sampler
        self.batch_size = batch_size
        self.drop_last = drop_last

    def __iter__(self) -> Iterator[List[int]]:
        batch = []
        for idx in self.sampler:
            batch.append(idx)
            if len(batch) == self.batch_size:
                yield batch
                batch = []
        if batch and not self.drop_last:
            yield batch

    def __len__(self) -> int:
        if self.drop_last:
            return len(self.sampler) // self.batch_size
        return (len(self.sampler) + self.batch_size - 1) // self.batch_size
