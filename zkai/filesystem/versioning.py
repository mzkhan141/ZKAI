"""VersionedStorage and FileRelationshipGraph for AI File System."""

from typing import Any, Dict, List, Optional
from zkai.storage.blob import BlobStore
from zkai.memory.knowledge_graph import KnowledgeGraph
from zkai.filesystem.files import SemanticFile
from zkai.core.logger import get_logger

logger = get_logger("filesystem.versioning")


class VersionedStorage:
    """Content-addressable versioning for SemanticFiles backed by BlobStore."""

    def __init__(self):
        self.blob_store = BlobStore()
        self.version_history: Dict[str, List[str]] = {}

    def commit(self, filename: str, data: bytes) -> str:
        content_hash = self.blob_store.put(data)
        if filename not in self.version_history:
            self.version_history[filename] = []
        self.version_history[filename].append(content_hash)
        logger.info(f"Committed '{filename}' version {len(self.version_history[filename])} (hash: {content_hash[:8]})")
        return content_hash

    def get_version(self, filename: str, version_index: int = -1) -> Optional[bytes]:
        if filename not in self.version_history or not self.version_history[filename]:
            return None
        content_hash = self.version_history[filename][version_index]
        return self.blob_store.get(content_hash)


class FileRelationshipGraph:
    """Tracks graph connections and dependencies between SemanticFiles using KnowledgeGraph."""

    def __init__(self):
        self.kg = KnowledgeGraph()

    def add_relationship(self, source_file: SemanticFile, target_file: SemanticFile, relation: str = "depends_on") -> None:
        self.kg.add_node(source_file.name, label="SemanticFile", properties=source_file.metadata)
        self.kg.add_node(target_file.name, label="SemanticFile", properties=target_file.metadata)
        self.kg.add_edge(source_file.name, target_file.name, relation=relation)
        source_file.relationships.append(f"{relation}:{target_file.name}")

    def get_related(self, filename: str) -> List[str]:
        nodes = self.kg.traverse(filename)
        return [n.id for n in nodes if n.id != filename]
