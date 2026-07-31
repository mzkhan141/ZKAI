"""Unit tests for Knowledge Base subsystem."""

import pytest
from zkai.knowledge import (
    KnowledgeBase,
    KnowledgeEntry,
    MarkdownVault,
    Notebook,
    Reference,
    ReferenceManager,
    SnippetManager,
    Wiki,
)


def test_knowledge_base():
    kb = KnowledgeBase()
    entry = KnowledgeEntry(id="1", title="Test Entry", content="Some test info", tags=["ai"])
    kb.add_entry(entry)
    assert kb.get_entry("1") == entry
    assert len(kb.search_by_tag("ai")) == 1


def test_wiki():
    wiki = Wiki()
    page = wiki.create_page("Neural Networks", "# Neural Networks\nDetails here...")
    assert page.title == "Neural Networks"
    assert page.id == "neural_networks"


def test_snippet_manager():
    sm = SnippetManager()
    sm.save_snippet("fn", "def foo(): pass")
    assert sm.get_snippet("fn") == "def foo(): pass"
