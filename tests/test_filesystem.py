"""Tests for AI Semantic Filesystem."""

import pytest
from zkai.filesystem.files import KnowledgeFile, ModelFile, SemanticFile
from zkai.filesystem.index import SemanticFileIndex
from zkai.filesystem.versioning import VersionedStorage, FileRelationshipGraph


def test_semantic_file_creation_and_hashing():
    kf = KnowledgeFile("architecture.md")
    assert kf.content_type == "application/x-zkai-knowledge"
    h = kf.compute_hash(b"# ZKAI Architecture")
    assert len(h) == 64


def test_semantic_file_index_and_search():
    index = SemanticFileIndex()
    f1 = KnowledgeFile("doc1.txt")
    f2 = KnowledgeFile("doc2.txt")

    index.index_file(f1, "Neural network deep learning transformers")
    index.index_file(f2, "Quantum mechanics and subatomic particles")

    results = index.search("Neural network deep learning transformers", top_k=2)
    assert len(results) >= 1
    assert any(r.name == "doc1.txt" for r in results)


def test_versioned_storage_and_relationship_graph():
    vs = VersionedStorage()
    hash1 = vs.commit("config.zk", b"v1_data")
    hash2 = vs.commit("config.zk", b"v2_data")

    assert vs.get_version("config.zk", 0) == b"v1_data"
    assert vs.get_version("config.zk", 1) == b"v2_data"

    graph = FileRelationshipGraph()
    f_src = ModelFile("llama.zk")
    f_tgt = KnowledgeFile("prompt.txt")
    graph.add_relationship(f_src, f_tgt, relation="uses_prompt")

    related = graph.get_related("llama.zk")
    assert "prompt.txt" in related
