"""MetricsLogger for step and epoch metrics tracking."""

from typing import Dict, List


class MetricsLogger:
    """Accumulates metrics history across training runs."""

    def __init__(self):
        self.history: Dict[str, List[float]] = {}

    def log(self, metric_name: str, value: float) -> None:
        if metric_name not in self.history:
            self.history[metric_name] = []
        self.history[metric_name].append(value)

    def get_latest(self, metric_name: str) -> float:
        if metric_name in self.history and self.history[metric_name]:
            return self.history[metric_name][-1]
        return 0.0
