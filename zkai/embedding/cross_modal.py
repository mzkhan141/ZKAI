"""CrossModalEmbedding projecting multiple modalities into shared embedding space."""

from typing import Any, List, Union
import torch
from zkai.embedding.model import EmbeddingModel
from zkai.embedding.text import TextEmbedding
from zkai.embedding.image import ImageEmbedding
from zkai.neural.tensor import Tensor
from zkai.core.types import EmbeddingModalityType


class CrossModalEmbedding(EmbeddingModel):
    """Shared cross-modal projection embedding space generator."""

    def __init__(self, dimension: int = 512):
        super().__init__(dimension=dimension, modality=EmbeddingModalityType.CROSS_MODAL)
        self.text_embedder = TextEmbedding(dimension=dimension)
        self.image_embedder = ImageEmbedding(dimension=dimension)

    def embed(self, inputs: Union[Any, List[Any]]) -> Tensor:
        items = [inputs] if not isinstance(inputs, list) else inputs
        batch_vecs = []
        for item in items:
            if isinstance(item, str):
                vec = self.text_embedder.embed(item).raw
            else:
                vec = self.image_embedder.embed(item).raw
            batch_vecs.append(vec.squeeze(0))
        return Tensor(torch.stack(batch_vecs))
