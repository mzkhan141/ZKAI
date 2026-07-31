"""Unified Multimodal Document container."""

from dataclasses import dataclass, field
from datetime import datetime
import uuid
from typing import Any, Dict, List, Optional
from zkai.core.types import DocumentType


@dataclass
class DocumentChunk:
    """A segment chunk extracted from a unified Document."""
    content: str
    chunk_index: int
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    metadata: Dict[str, Any] = field(default_factory=dict)
    embedding: Optional[List[float]] = None


@dataclass
class Document:
    """Unified Multimodal Document container."""
    content: str
    doc_type: DocumentType = DocumentType.TEXT
    file_path: Optional[str] = None
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    metadata: Dict[str, Any] = field(default_factory=dict)
    chunks: List[DocumentChunk] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
