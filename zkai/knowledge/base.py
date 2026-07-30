"""KnowledgeBase core entry store."""

from dataclasses import dataclass, field
import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class KnowledgeEntry:
    id: str
    title: str
    content: str
    category: str = "general"
    tags: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())


class KnowledgeBase:
    """Unified knowledge repository integrating structured documentation and notes."""

    def __init__(self, storage_dir: str = "./knowledge_store"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.entries: Dict[str, KnowledgeEntry] = {}

    def add_entry(self, entry: KnowledgeEntry) -> None:
        self.entries[entry.id] = entry

    def get_entry(self, entry_id: str) -> Optional[KnowledgeEntry]:
        return self.entries.get(entry_id)

    def search_by_tag(self, tag: str) -> List[KnowledgeEntry]:
        return [e for e in self.entries.values() if tag in e.tags]
