"""Timing Utilities, Stopwatch, and Decorators."""

import functools
import time
from typing import Any, Callable
from zkai.core.logger import get_logger

logger = get_logger("timing")


class Stopwatch:
    """High-precision stopwatch for timing code blocks."""

    def __init__(self):
        self._start_time: float = 0.0
        self._elapsed: float = 0.0
        self._running: bool = False

    def start(self) -> None:
        if not self._running:
            self._start_time = time.perf_counter()
            self._running = True

    def stop(self) -> float:
        if self._running:
            self._elapsed += time.perf_counter() - self._start_time
            self._running = False
        return self._elapsed

    def reset(self) -> None:
        self._start_time = 0.0
        self._elapsed = 0.0
        self._running = False

    @property
    def elapsed_seconds(self) -> float:
        if self._running:
            return self._elapsed + (time.perf_counter() - self._start_time)
        return self._elapsed


def timed(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator to measure and log execution time of any function."""
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        res = func(*args, **kwargs)
        duration = time.perf_counter() - start
        logger.debug(f"Function '{func.__qualname__}' executed in {duration:.4f}s")
        return res
    return wrapper
