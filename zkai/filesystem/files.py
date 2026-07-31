"""SemanticFile base class and specialized domain file objects for ZKAI AI File System."""

import hashlib
from pathlib import Path
from typing import Any, Dict, List, Optional
from zkai.core.logger import get_logger

logger = get_logger("filesystem.files")


class SemanticFile:
    """Base class for all searchable semantic files in ZKAI AI File System."""

    def __init__(self, filepath: str, content_type: str = "text/plain"):
        self.filepath = Path(filepath)
        self.name = self.filepath.name
        self.content_type = content_type
        self.content_hash: str = ""
        self.embedding_vector: Optional[List[float]] = None
        self.metadata: Dict[str, Any] = {}
        self.relationships: List[str] = []

    def compute_hash(self, content: bytes) -> str:
        self.content_hash = hashlib.sha256(content).hexdigest()
        return self.content_hash

    def extract_metadata(self, content: Any) -> Dict[str, Any]:
        """Extracts domain metadata from content."""
        self.metadata["size_bytes"] = len(content) if hasattr(content, "__len__") else 0
        return self.metadata


class KnowledgeFile(SemanticFile):
    """Semantic file wrapping KnowledgeBase markdown/text articles."""

    def __init__(self, filepath: str):
        super().__init__(filepath, content_type="application/x-zkai-knowledge")


class MemoryFile(SemanticFile):
    """Semantic file wrapping persistent memory snapshots."""

    def __init__(self, filepath: str):
        super().__init__(filepath, content_type="application/x-zkai-memory")


class ModelFile(SemanticFile):
    """Semantic file wrapping .zk, gguf, or safetensors weight binaries."""

    def __init__(self, filepath: str):
        super().__init__(filepath, content_type="application/x-zkai-model")


class PluginFile(SemanticFile):
    """Semantic file wrapping plugin modules or manifests."""

    def __init__(self, filepath: str):
        super().__init__(filepath, content_type="application/x-zkai-plugin")


class TaskFile(SemanticFile):
    """Semantic file wrapping scheduled Task records."""

    def __init__(self, filepath: str):
        super().__init__(filepath, content_type="application/x-zkai-task")


class WorkflowFile(SemanticFile):
    """Semantic file wrapping DAG workflow JSON definitions."""

    def __init__(self, filepath: str):
        super().__init__(filepath, content_type="application/x-zkai-workflow")


class ConversationFile(SemanticFile):
    """Semantic file wrapping chat session histories."""

    def __init__(self, filepath: str):
        super().__init__(filepath, content_type="application/x-zkai-conversation")


class ImageFile(SemanticFile):
    """Semantic file wrapping image assets."""

    def __init__(self, filepath: str):
        super().__init__(filepath, content_type="image/png")


class AudioFile(SemanticFile):
    """Semantic file wrapping audio assets."""

    def __init__(self, filepath: str):
        super().__init__(filepath, content_type="audio/wav")


class VideoFile(SemanticFile):
    """Semantic file wrapping video assets."""

    def __init__(self, filepath: str):
        super().__init__(filepath, content_type="video/mp4")


class ProjectFile(SemanticFile):
    """Semantic file wrapping workspace project trees."""

    def __init__(self, filepath: str):
        super().__init__(filepath, content_type="application/x-zkai-project")
