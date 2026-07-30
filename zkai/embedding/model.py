"""EmbeddingModel ABC for text, vision, audio, and multimodal vector embedding generators."""

from abc import ABC, abstractmethod
from typing import Any, List, Union
import torch
from zkai.neural.tensor import Tensor
from zkai.core.types import EmbeddingModalityType


class EmbeddingModel(ABC):
    """Abstract Base Class for all modality embedding generators."""

    def __init__(self, dimension: int = 384, modality: EmbeddingModalityType = EmbeddingModalityType.TEXT):
        self.dimension = dimension
        self.modality = modality

    @abstractmethod
    def embed(self, inputs: Union[Any, List[Any]]) -> Tensor:
        """Generates embedding vectors for single input or batch of inputs."""
        pass
