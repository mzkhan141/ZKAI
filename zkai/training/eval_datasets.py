"""Evaluation datasets and validation benchmark datasets for training loops."""

from typing import Any, List, Tuple
from zkai.training.dataset import Dataset, SimpleDataset


class EvalDataset(Dataset):
    """Base Evaluation Dataset."""

    def __init__(self, samples: List[Tuple[Any, Any]]):
        self.samples = samples

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, idx: int) -> Tuple[Any, Any]:
        return self.samples[idx]


class PerplexityEvalDataset(EvalDataset):
    """Text sequence dataset for language model perplexity evaluation."""

    def __init__(self, text_sequences: List[str]):
        samples = [(seq, seq) for seq in text_sequences]
        super().__init__(samples)
