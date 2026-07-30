"""Persistent Knowledge Base Subsystem for ZKAI."""

from zkai.knowledge.base import KnowledgeBase, KnowledgeEntry
from zkai.knowledge.indexer import EmbeddingIndexer
from zkai.knowledge.notebook import Notebook, NotebookCell
from zkai.knowledge.pdf_library import PDFLibrary
from zkai.knowledge.references import Reference, ReferenceManager
from zkai.knowledge.search import SemanticSearch
from zkai.knowledge.snippets import SnippetManager
from zkai.knowledge.vault import MarkdownVault
from zkai.knowledge.versioning import KnowledgeRevision, VersionHistory
from zkai.knowledge.wiki import Wiki
from zkai.knowledge.governance import (
    KnowledgeGovernor,
    ProvenanceTracker,
    CitationEngine,
    KnowledgeLineage,
    ConfidenceScorer,
    ConflictResolver,
    FactVerification,
    TrustManager,
    KnowledgeVersioning,
    KnowledgeAuditor,
    SourceTracking,
    RelationshipValidation,
)

__all__ = [
    "KnowledgeEntry",
    "KnowledgeBase",
    "Wiki",
    "MarkdownVault",
    "PDFLibrary",
    "NotebookCell",
    "Notebook",
    "SnippetManager",
    "Reference",
    "ReferenceManager",
    "EmbeddingIndexer",
    "SemanticSearch",
    "KnowledgeRevision",
    "VersionHistory",
    "KnowledgeGovernor",
    "ProvenanceTracker",
    "CitationEngine",
    "KnowledgeLineage",
    "ConfidenceScorer",
    "ConflictResolver",
    "FactVerification",
    "TrustManager",
    "KnowledgeVersioning",
    "KnowledgeAuditor",
    "SourceTracking",
    "RelationshipValidation",
]
