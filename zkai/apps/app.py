"""AIApplication framework allowing third-party AI Applications on ZKAI."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from zkai.core.plugin import Plugin, PluginMetadata, PluginSandbox
from zkai.security.permissions import PermissionManager
from zkai.core.logger import get_logger

logger = get_logger("apps")


@dataclass
class ApplicationPermissions:
    """Declared capabilities requested by an AIApplication."""
    requested_capabilities: List[str] = field(default_factory=list)


@dataclass
class ApplicationManifest:
    """Manifest describing an AIApplication package."""
    app_id: str
    name: str
    version: str
    description: str
    author: str
    entry_point: str
    permissions: ApplicationPermissions = field(default_factory=ApplicationPermissions)


class ApplicationLifecycle:
    """Drives installation, configuration, launch, pause, and teardown lifecycles."""

    def __init__(self, manifest: ApplicationManifest):
        self.manifest = manifest
        self.is_running: bool = False

    def start(self) -> None:
        self.is_running = True
        logger.info(f"Started AIApplication '{self.manifest.name}' v{self.manifest.version}")

    def stop(self) -> None:
        self.is_running = False
        logger.info(f"Stopped AIApplication '{self.manifest.name}'")


class ApplicationSandbox:
    """Sandbox evaluating app security permissions before runtime execution."""

    def __init__(self, permission_manager: Optional[PermissionManager] = None):
        self.permission_manager = permission_manager or PermissionManager()

    def validate_app(self, manifest: ApplicationManifest) -> bool:
        for cap in manifest.permissions.requested_capabilities:
            if not self.permission_manager.check("agent", cap):
                logger.warning(f"Application '{manifest.app_id}' denied capability '{cap}'")
                return False
        return True


class ApplicationRuntime:
    """Execution runtime environment injecting ZKAI OS services into AIApplications."""

    def __init__(self, app_context: Any = None):
        self.app_context = app_context

    def run_app(self, app: "AIApplication") -> Any:
        logger.info(f"Running AIApplication '{app.manifest.name}' in ApplicationRuntime")
        return app.run(self.app_context)


class AIApplication(Plugin):
    """Abstract base class for third-party AI Applications built on ZKAI."""

    def __init__(self, manifest: ApplicationManifest):
        meta = PluginMetadata(
            name=manifest.name,
            version=manifest.version,
            description=manifest.description,
            author=manifest.author,
        )
        super().__init__(metadata=meta)
        self.manifest = manifest
        self.lifecycle = ApplicationLifecycle(manifest)

    def initialize(self, app_context: Any) -> None:
        logger.info(f"Initializing AIApplication '{self.manifest.name}'...")

    def shutdown(self) -> None:
        self.lifecycle.stop()

    def run(self, app_context: Any) -> Any:
        self.lifecycle.start()
        return f"AIApplication '{self.manifest.name}' executed successfully."
