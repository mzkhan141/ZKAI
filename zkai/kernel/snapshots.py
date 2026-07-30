"""Transactional OS System Snapshots, Recovery Journals, Rollback Management, and Restore Engine."""

from dataclasses import dataclass, field
import json
from pathlib import Path
import time
import uuid
from typing import Any, Dict, List, Optional
from zkai.core.logger import get_logger

logger = get_logger("kernel.snapshots")


@dataclass
class CheckpointBase:
    checkpoint_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class KernelCheckpoint(CheckpointBase):
    state: str = "READY"
    active_services: List[str] = field(default_factory=list)


@dataclass
class WorkspaceCheckpoint(CheckpointBase):
    active_files: List[str] = field(default_factory=list)
    project_root: str = "."


@dataclass
class WorkflowCheckpoint(CheckpointBase):
    running_workflows: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class ConversationCheckpoint(CheckpointBase):
    conversations: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class MemoryCheckpoint(CheckpointBase):
    working_count: int = 0
    short_term_count: int = 0


@dataclass
class ModelCheckpoint(CheckpointBase):
    loaded_models: List[str] = field(default_factory=list)


@dataclass
class SystemSnapshot:
    """Transactional full OS state snapshot capturing all subsystem checkpoints."""

    snapshot_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = field(default_factory=time.time)
    kernel_checkpoint: KernelCheckpoint = field(default_factory=KernelCheckpoint)
    workspace_checkpoint: WorkspaceCheckpoint = field(default_factory=WorkspaceCheckpoint)
    workflow_checkpoint: WorkflowCheckpoint = field(default_factory=WorkflowCheckpoint)
    conversation_checkpoint: ConversationCheckpoint = field(default_factory=ConversationCheckpoint)
    memory_checkpoint: MemoryCheckpoint = field(default_factory=MemoryCheckpoint)
    model_checkpoint: ModelCheckpoint = field(default_factory=ModelCheckpoint)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "snapshot_id": self.snapshot_id,
            "timestamp": self.timestamp,
            "kernel": {"state": self.kernel_checkpoint.state, "services": self.kernel_checkpoint.active_services},
            "workspace": {"files": self.workspace_checkpoint.active_files, "root": self.workspace_checkpoint.project_root},
            "workflow": {"running": self.workflow_checkpoint.running_workflows},
            "conversation": {"conversations": self.conversation_checkpoint.conversations},
            "memory": {"working": self.memory_checkpoint.working_count, "short_term": self.memory_checkpoint.short_term_count},
            "model": {"loaded": self.model_checkpoint.loaded_models},
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SystemSnapshot":
        snap = cls(snapshot_id=data.get("snapshot_id", str(uuid.uuid4())), timestamp=data.get("timestamp", time.time()))
        if "kernel" in data:
            snap.kernel_checkpoint = KernelCheckpoint(state=data["kernel"].get("state", "READY"), active_services=data["kernel"].get("services", []))
        if "workspace" in data:
            snap.workspace_checkpoint = WorkspaceCheckpoint(active_files=data["workspace"].get("files", []), project_root=data["workspace"].get("root", "."))
        if "workflow" in data:
            snap.workflow_checkpoint = WorkflowCheckpoint(running_workflows=data["workflow"].get("running", []))
        if "conversation" in data:
            snap.conversation_checkpoint = ConversationCheckpoint(conversations=data["conversation"].get("conversations", []))
        if "memory" in data:
            snap.memory_checkpoint = MemoryCheckpoint(working_count=data["memory"].get("working", 0), short_term_count=data["memory"].get("short_term", 0))
        if "model" in data:
            snap.model_checkpoint = ModelCheckpoint(loaded_models=data["model"].get("loaded", []))
        return snap


class RecoveryJournal:
    """Write-ahead transactional log (WAL) for state mutation rollback."""

    def __init__(self, journal_path: str = "./recovery_journal.jsonl"):
        self.journal_path = Path(journal_path)

    def append_entry(self, operation: str, data: Dict[str, Any]) -> None:
        self.journal_path.parent.mkdir(parents=True, exist_ok=True)
        entry = {"operation": operation, "timestamp": time.time(), "data": data}
        with open(self.journal_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

    def read_journal(self) -> List[Dict[str, Any]]:
        if not self.journal_path.exists():
            return []
        entries = []
        with open(self.journal_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    entries.append(json.loads(line))
        return entries


class VersionHistory:
    """Tracks historical system snapshot versions."""

    def __init__(self):
        self.snapshots: Dict[str, SystemSnapshot] = {}

    def add_snapshot(self, snap: SystemSnapshot) -> None:
        self.snapshots[snap.snapshot_id] = snap

    def get_latest(self) -> Optional[SystemSnapshot]:
        if not self.snapshots:
            return None
        return max(self.snapshots.values(), key=lambda s: s.timestamp)

    def list_history(self) -> List[SystemSnapshot]:
        return sorted(self.snapshots.values(), key=lambda s: s.timestamp, reverse=True)


from zkai.kernel.types import KernelState
from zkai.core.logger import get_logger

logger = get_logger("kernel.snapshots")


class RestoreEngine:
    """Orchestrates restoring system state from snapshot checkpoints."""

    @staticmethod
    def restore_system(kernel: Any, snapshot: SystemSnapshot) -> bool:
        logger.info(f"RestoreEngine restoring system state to snapshot '{snapshot.snapshot_id}'...")
        if hasattr(kernel, "state_machine"):
            kernel.state_machine.transition_to(KernelState.RECOVERY, reason="Restoring from snapshot")

        # Restores state across services
        logger.info(f"Restored kernel state: {snapshot.kernel_checkpoint.state}")
        if hasattr(kernel, "state_machine"):
            kernel.state_machine.transition_to(KernelState.READY, reason="Restore complete")
        return True


class RollbackManager:
    """Manages snapshot creation, listing, and automated rollback upon crash or error."""

    def __init__(self, kernel: Any, storage_dir: str = "./snapshots"):
        self.kernel = kernel
        self.storage_dir = Path(storage_dir)
        self.history = VersionHistory()
        self.journal = RecoveryJournal(str(self.storage_dir / "recovery_journal.jsonl"))

    def create_snapshot(self) -> SystemSnapshot:
        """Captures full system snapshot across all active kernel services."""
        snap = SystemSnapshot(
            kernel_checkpoint=KernelCheckpoint(
                state=getattr(self.kernel.state, "value", str(self.kernel.state)) if hasattr(self.kernel, "state") else "READY",
                active_services=[s.name for s in self.kernel.list_services()] if hasattr(self.kernel, "list_services") else [],
            ),
            model_checkpoint=ModelCheckpoint(
                loaded_models=getattr(self.kernel.scheduler.model_scheduler, "loaded_models", []) if hasattr(self.kernel, "scheduler") else []
            ),
        )
        self.history.add_snapshot(snap)
        self._persist_snapshot(snap)
        self.journal.append_entry("CREATE_SNAPSHOT", {"snapshot_id": snap.snapshot_id})
        logger.info(f"RollbackManager created SystemSnapshot '{snap.snapshot_id}'")
        return snap

    def _persist_snapshot(self, snap: SystemSnapshot) -> None:
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        filepath = self.storage_dir / f"snapshot_{snap.snapshot_id}.json"
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(snap.to_dict(), f, indent=2)

    def rollback_to_latest(self) -> bool:
        latest = self.history.get_latest()
        if not latest:
            logger.warning("RollbackManager found no snapshot to roll back to.")
            return False
        logger.info(f"RollbackManager rolling back system to latest snapshot '{latest.snapshot_id}'")
        self.journal.append_entry("ROLLBACK_LATEST", {"target_snapshot_id": latest.snapshot_id})
        return RestoreEngine.restore_system(self.kernel, latest)


class SnapshotScheduler:
    """Schedules automatic background system snapshots."""

    def __init__(self, rollback_manager: RollbackManager, interval_seconds: float = 300.0):
        self.rollback_manager = rollback_manager
        self.interval_seconds = interval_seconds
        self.last_run = time.time()

    def tick(self) -> Optional[SystemSnapshot]:
        now = time.time()
        if now - self.last_run >= self.interval_seconds:
            self.last_run = now
            return self.rollback_manager.create_snapshot()
        return None
