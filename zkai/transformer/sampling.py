"""Sampling Strategies (Greedy, BeamSearch, TopK, TopP, Temperature, RepetitionPenalty)."""

from typing import List, Tuple, Optional
import torch
import torch.nn.functional as F
from zkai.neural.tensor import Tensor


class Sampler:
    """Base class for output token sampling."""

    def sample(self, logits: Tensor) -> int:
        raise NotImplementedError


class GreedySampler(Sampler):
    """Selects the token with maximum probability."""

    def sample(self, logits: Tensor) -> int:
        return int(torch.argmax(logits.raw, dim=-1).item())


class TemperatureSampler(Sampler):
    """Scales logits by temperature parameter before sampling."""

    def __init__(self, temperature: float = 0.7):
        self.temperature = max(1e-5, temperature)

    def sample(self, logits: Tensor) -> int:
        scaled_logits = logits.raw / self.temperature
        probs = F.softmax(scaled_logits, dim=-1)
        return int(torch.multinomial(probs, num_samples=1).item())


class TopKSampler(Sampler):
    """Restricts sampling to the top K highest probability tokens."""

    def __init__(self, k: int = 50, temperature: float = 0.7):
        self.k = k
        self.temperature = max(1e-5, temperature)

    def sample(self, logits: Tensor) -> int:
        scaled_logits = logits.raw / self.temperature
        top_k_logits, top_k_indices = torch.topk(scaled_logits, self.k, dim=-1)
        probs = F.softmax(top_k_logits, dim=-1)
        sampled_idx = torch.multinomial(probs, num_samples=1).item()
        return int(top_k_indices[..., sampled_idx].item())


class TopPSampler(Sampler):
    """Nucleus Sampling: filters out tokens below cumulative probability p."""

    def __init__(self, p: float = 0.9, temperature: float = 0.7):
        self.p = p
        self.temperature = max(1e-5, temperature)

    def sample(self, logits: Tensor) -> int:
        scaled_logits = logits.raw / self.temperature
        sorted_logits, sorted_indices = torch.sort(scaled_logits, descending=True, dim=-1)
        cumulative_probs = torch.cumsum(F.softmax(sorted_logits, dim=-1), dim=-1)

        sorted_indices_to_remove = cumulative_probs > self.p
        sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()
        sorted_indices_to_remove[..., 0] = 0

        indices_to_remove = sorted_indices_to_remove.scatter(dim=-1, index=sorted_indices, src=sorted_indices_to_remove)
        scaled_logits[indices_to_remove] = -float("Inf")

        probs = F.softmax(scaled_logits, dim=-1)
        return int(torch.multinomial(probs, num_samples=1).item())


class RepetitionPenalty:
    """Applies multiplicative penalty to logits of previously generated token IDs."""

    @staticmethod
    def apply(logits: torch.Tensor, generated_tokens: List[int], penalty: float = 1.1) -> torch.Tensor:
        if not generated_tokens or penalty == 1.0:
            return logits
        for token in set(generated_tokens):
            if logits[0, token] < 0:
                logits[0, token] *= penalty
            else:
                logits[0, token] /= penalty
        return logits


class BeamSearch:
    """Beam search decoding for sequence generation."""

    def __init__(self, beam_width: int = 4):
        self.beam_width = beam_width
