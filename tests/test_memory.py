"""Unit tests for zkai.memory subsystem."""

import pytest
from zkai.memory.manager import MemoryManager
from zkai.memory.working import WorkingMemory
from zkai.memory.knowledge_graph import KnowledgeGraph


def test_working_memory():
    wm = WorkingMemory(capacity=2)
    wm.store("k1", "content 1")
    wm.store("k2", "content 2")
    assert len(wm.get_all()) == 2
    wm.store("k3", "content 3")
    # k1 evicted
    assert len(wm.get_all()) == 2
    assert wm.get_all()[-1].key == "k3"


def test_knowledge_graph():
    kg = KnowledgeGraph()
    n1 = kg.add_node("AI", label="Artificial Intelligence")
    n2 = kg.add_node("ZKAI", label="ZKAI Framework")
    kg.add_edge("ZKAI", "AI", relation="is_a")

    traversal = kg.traverse("ZKAI", max_depth=1)
    assert len(traversal) >= 1


def test_memory_manager(temp_dir):
    mm = MemoryManager(persistence_dir=str(temp_dir / "mem"))
    mm.remember("user_preference", "Dark Mode")
    results = mm.search("preference")
    assert len(results) > 0
    assert "Dark Mode" in str(results[0].content)
