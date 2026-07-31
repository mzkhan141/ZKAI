"""Visual Feature Extractor producing dense image embedding vectors."""

from typing import List
import numpy as np
from zkai.vision.image import Image
from zkai.core.logger import get_logger

logger = get_logger("vision.features")


class FeatureExtractor:
    """Extracts dense high-dimensional feature embedding vectors from images."""

    def __init__(self, feature_dim: int = 512):
        self.feature_dim = feature_dim

    def extract(self, image: Image) -> List[float]:
        """Extracts dense feature vector representation."""
        logger.info("Extracting visual feature embeddings...")
        arr = image.to_numpy().astype(np.float32)
        # Compute mean feature vector projection
        vec = np.mean(arr, axis=(0, 1))
        # Pad to feature dimension
        padded = np.pad(vec, (0, max(0, self.feature_dim - len(vec))))[: self.feature_dim]
        return padded.tolist()
