"""VersionHistory for tracking revision history of knowledge entries."""

from dataclasses import dataclass, field
import datetime
from typing import Dict, List


@dataclass
class KnowledgeRevision:
    revision_id: int
    content: str
    timestamp: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())


class VersionHistory:
    """Tracks edit revisions and history diffs for knowledge documents."""

    def __init__(self):
        self.history: Dict[str, List[KnowledgeRevision]] = {}

    def commit(self, entry_id: str, content: str) -> None:
        if entry_id not in self.history:
            self.history[entry_id] = []
        rev_id = len(self.history[entry_id]) + 1
        self.history[entry_id].append(KnowledgeRevision(revision_id=rev_id, content=content))
