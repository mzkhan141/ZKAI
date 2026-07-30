"""EvalBenchmark ABC and EvalResult data structure for LLM evaluation suites."""

import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from zkai.core.logger import get_logger

logger = get_logger("llm_eval.base")


@dataclass
class EvalResult:
    """Evaluation result container for benchmark runs."""

    benchmark_name: str
    score: float  # Percentage accuracy (0.0 to 100.0)
    total_samples: int
    passed_samples: int
    subcategories: Dict[str, float] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


class EvalBenchmark(ABC):
    """Abstract Base Class for standard LLM benchmark suites."""

    def __init__(self, dataset_path: Optional[Union[str, Path]] = None):
        self.dataset_path = Path(dataset_path) if dataset_path else None

    def load_external_dataset(self) -> List[Dict[str, Any]]:
        """Loads evaluation dataset from external file path (.json / .jsonl)."""
        if not self.dataset_path or not self.dataset_path.exists():
            logger.info(f"No external dataset found at {self.dataset_path}, using built-in evaluation schema.")
            return self._get_fallback_data()

        samples = []
        if self.dataset_path.suffix.lower() == ".jsonl":
            with open(self.dataset_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        samples.append(json.loads(line))
        else:
            with open(self.dataset_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                samples = data if isinstance(data, list) else [data]
        return samples

    @abstractmethod
    def _get_fallback_data(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def evaluate(self, model: Any) -> EvalResult:
        pass
