"""Unit tests for Documentation Generator subsystem."""

import pytest
from zkai.docs import APIDocGenerator, ArchitectureDocGenerator, DeveloperGuideGenerator


def test_api_doc_generator():
    gen = APIDocGenerator()
    doc = gen.generate_class_doc(APIDocGenerator)
    assert "# Class `APIDocGenerator`" in doc


def test_architecture_doc_generator():
    gen = ArchitectureDocGenerator()
    doc = gen.generate_architecture_doc()
    assert "# ZKAI Framework Architecture" in doc
