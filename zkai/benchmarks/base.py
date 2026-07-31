"""Benchmark base classes and report structures."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import datetime
from typing import Any, Dict


@dataclass
class BenchmarkResult:
    benchmark_name: str
    score: float
    metrics: Dict[str, float] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())


class Benchmark(ABC):
    """Abstract Base Class for ZKAI Benchmark suites."""

    @abstractmethod
    def run(self, target: Any) -> BenchmarkResult:
        pass
