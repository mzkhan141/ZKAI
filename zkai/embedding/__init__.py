"""Embedding Framework Subsystem for ZKAI."""

from zkai.embedding.audio import AudioEmbedding
from zkai.embedding.cross_modal import CrossModalEmbedding
from zkai.embedding.image import ImageEmbedding
from zkai.embedding.index import SemanticSearch, SimilarityIndex
from zkai.embedding.model import EmbeddingModel
from zkai.embedding.text import TextEmbedding
from zkai.embedding.trainer import EmbeddingTrainer
from zkai.embedding.video import VideoEmbedding

__all__ = [
    "EmbeddingModel",
    "TextEmbedding",
    "ImageEmbedding",
    "AudioEmbedding",
    "VideoEmbedding",
    "CrossModalEmbedding",
    "EmbeddingTrainer",
    "SimilarityIndex",
    "SemanticSearch",
]
