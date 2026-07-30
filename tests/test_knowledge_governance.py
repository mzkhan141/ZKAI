"""Unit tests for Knowledge Governance, Provenance Tracking, and Citations."""

import pytest
from zkai.knowledge import (
    CitationEngine,
    KnowledgeGovernor,
    ProvenanceTracker,
    TrustManager,
)


def test_provenance_tracker():
    tracker = ProvenanceTracker()
    rec = tracker.track("fact_1", origin="user_chat", confidence=0.95)
    assert rec.origin == "user_chat"
    assert rec.confidence == 0.95


def test_citation_formatting():
    tracker = ProvenanceTracker()
    rec = tracker.track("fact_2", origin="wikipedia", confidence=0.8)
    citation = CitationEngine.format_citation(rec)
    assert "wikipedia" in citation
    assert "0.80" in citation


def test_knowledge_governor_ingest():
    governor = KnowledgeGovernor()
    rec = governor.ingest("entry_100", "Quantum computing accelerates search.", source="system")
    assert rec.confidence == 1.0
    assert "entry_100" in governor.provenance.records
