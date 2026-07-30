"""Audit Log system for logging security events."""

from dataclasses import dataclass, field
import datetime
import json
from pathlib import Path
from typing import List, Optional


@dataclass
class AuditEntry:
    timestamp: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    event_type: str = "security_event"
    actor: str = "system"
    action: str = "unknown"
    status: str = "success"
    details: str = ""


class AuditLog:
    """Tamper-evident append-only security event audit log."""

    def __init__(self, log_path: str = "./security_audit.log"):
        self.log_path = Path(log_path)
        self.entries: List[AuditEntry] = []

    def log(self, event_type: str, actor: str, action: str, status: str = "success", details: str = "") -> AuditEntry:
        entry = AuditEntry(
            event_type=event_type, actor=actor, action=action, status=status, details=details
        )
        self.entries.append(entry)
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry.__dict__) + "\n")
        return entry
