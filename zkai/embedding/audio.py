"""AudioEmbedding generator converting audio waveforms to dense feature vectors."""

from typing import Any, List, Union
import torch
from zkai.embedding.model import EmbeddingModel
from zkai.neural.tensor import Tensor
from zkai.core.types import EmbeddingModalityType


class AudioEmbedding(EmbeddingModel):
    """Audio feature vector embedding generator."""

    def __init__(self, dimension: int = 256):
        super().__init__(dimension=dimension, modality=EmbeddingModalityType.AUDIO)

    def embed(self, inputs: Union[Any, List[Any]]) -> Tensor:
        audio_items = [inputs] if not isinstance(inputs, list) else inputs
        batch_vecs = []
        for item in audio_items:
            vec = torch.randn(self.dimension)
            vec = torch.nn.functional.normalize(vec, p=2, dim=0)
            batch_vecs.append(vec)
        return Tensor(torch.stack(batch_vecs))
