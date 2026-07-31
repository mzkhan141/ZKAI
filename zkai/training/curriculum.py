"""CurriculumLearning for dynamic data pacing and difficulty scheduling."""

from typing import Any, Callable, List, Optional, Tuple
from zkai.core.logger import get_logger

logger = get_logger("training.curriculum")


class CurriculumLearning:
    """Curriculum learning manager pacing datasets from easy to complex samples."""

    def __init__(self, scoring_fn: Optional[Callable[[Any], float]] = None):
        self.scoring_fn = scoring_fn or self._default_length_scorer

    @staticmethod
    def _default_length_scorer(sample: Any) -> float:
        if isinstance(sample, str):
            return float(len(sample.split()))
        elif isinstance(sample, (list, tuple)):
            return float(len(sample))
        return 1.0

    def sort_by_difficulty(self, dataset: List[Any], reverse: bool = False) -> List[Any]:
        """Sorts dataset items by computed difficulty score."""
        scored = [(self.scoring_fn(item), item) for item in dataset]
        scored.sort(key=lambda x: x[0], reverse=reverse)
        return [item for _, item in scored]

    def get_pacing_slice(self, dataset: List[Any], current_epoch: int, total_epochs: int) -> List[Any]:
        """Returns subset of dataset paced according to current epoch progress."""
        ratio = min(1.0, current_epoch / max(1, total_epochs))
        sample_count = max(1, int(len(dataset) * ratio))
        sorted_ds = self.sort_by_difficulty(dataset)
        return sorted_ds[:sample_count]
