"""Tests for Embedding Framework modules."""

import pytest
from zkai.embedding.text import TextEmbedding
from zkai.embedding.image import ImageEmbedding
from zkai.embedding.audio import AudioEmbedding
from zkai.embedding.video import VideoEmbedding
from zkai.embedding.cross_modal import CrossModalEmbedding
from zkai.embedding.index import SimilarityIndex, SemanticSearch


def test_text_embedding():
    embedder = TextEmbedding(dimension=128)
    res = embedder.embed("Artificial Intelligence Operating System")
    assert res.shape[1] == 128


def test_multimodal_embeddings():
    img_emb = ImageEmbedding(dimension=256).embed(["dummy_image"])
    assert img_emb.shape[1] == 256

    aud_emb = AudioEmbedding(dimension=128).embed(["dummy_audio"])
    assert aud_emb.shape[1] == 128


def test_semantic_search():
    searcher = SemanticSearch()
    searcher.add_documents(["Deep learning frameworks", "Quantum physics equations", "Machine learning algorithms"])
    results = searcher.search("AI neural networks", top_k=2)
    assert len(results) == 2
