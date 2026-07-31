"""ImageEmbedding generator converting images to dense feature vectors."""

from typing import Any, List, Union
import torch
from zkai.embedding.model import EmbeddingModel
from zkai.neural.tensor import Tensor
from zkai.core.types import EmbeddingModalityType


class ImageEmbedding(EmbeddingModel):
    """Image feature vector embedding generator."""

    def __init__(self, dimension: int = 512):
        super().__init__(dimension=dimension, modality=EmbeddingModalityType.IMAGE)

    def embed(self, inputs: Union[Any, List[Any]]) -> Tensor:
        images = [inputs] if not isinstance(inputs, list) else inputs
        batch_vecs = []
        for img in images:
            vec = torch.randn(self.dimension)
            vec = torch.nn.functional.normalize(vec, p=2, dim=0)
            batch_vecs.append(vec)
        return Tensor(torch.stack(batch_vecs))
