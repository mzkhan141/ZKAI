"""Metrics Collection Infrastructure (Counter, Gauge, Histogram)."""

from typing import Dict, List, Any
import time


class Counter:
    """Monotonically increasing counter metric."""

    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.value: float = 0.0

    def inc(self, amount: float = 1.0) -> None:
        if amount < 0:
            raise ValueError("Counter cannot be decremented")
        self.value += amount


class Gauge:
    """Gauge metric supporting values that move up and down."""

    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.value: float = 0.0

    def set(self, value: float) -> None:
        self.value = value

    def inc(self, amount: float = 1.0) -> None:
        self.value += amount

    def dec(self, amount: float = 1.0) -> None:
        self.value -= amount


class Histogram:
    """Histogram tracking distribution of floating point values."""

    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.values: List[float] = []

    def observe(self, value: float) -> None:
        self.values.append(value)

    def count(self) -> int:
        return len(self.values)

    def mean(self) -> float:
        return sum(self.values) / len(self.values) if self.values else 0.0


class MetricsCollector:
    """Central Manager collecting system and model performance metrics."""

    def __init__(self):
        self._counters: Dict[str, Counter] = {}
        self._gauges: Dict[str, Gauge] = {}
        self._histograms: Dict[str, Histogram] = {}

    def counter(self, name: str, description: str = "") -> Counter:
        if name not in self._counters:
            self._counters[name] = Counter(name, description)
        return self._counters[name]

    def gauge(self, name: str, description: str = "") -> Gauge:
        if name not in self._gauges:
            self._gauges[name] = Gauge(name, description)
        return self._gauges[name]

    def histogram(self, name: str, description: str = "") -> Histogram:
        if name not in self._histograms:
            self._histograms[name] = Histogram(name, description)
        return self._histograms[name]
