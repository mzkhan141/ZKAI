"""ApplicationRegistry and ApplicationStore for AI Applications."""

from typing import Dict, List, Optional
from zkai.apps.app import AIApplication, ApplicationManifest
from zkai.core.logger import get_logger

logger = get_logger("apps.registry")


class ApplicationRegistry:
    """Registry maintaining active registered AIApplications."""

    def __init__(self):
        self._apps: Dict[str, AIApplication] = {}

    def register(self, app: AIApplication) -> None:
        self._apps[app.manifest.app_id] = app
        logger.info(f"Registered AIApplication '{app.manifest.name}' ({app.manifest.app_id})")

    def unregister(self, app_id: str) -> None:
        if app_id in self._apps:
            del self._apps[app_id]

    def get(self, app_id: str) -> Optional[AIApplication]:
        return self._apps.get(app_id)

    def list_apps(self) -> List[ApplicationManifest]:
        return [app.manifest for app in self._apps.values()]


class ApplicationStore:
    """Local storage catalog for installed AIApplications."""

    def __init__(self):
        self.registry = ApplicationRegistry()

    def install_app(self, app: AIApplication) -> None:
        self.registry.register(app)

    def uninstall_app(self, app_id: str) -> None:
        self.registry.unregister(app_id)

    def search_apps(self, query: str) -> List[ApplicationManifest]:
        results = []
        for manifest in self.registry.list_apps():
            if query.lower() in manifest.name.lower() or query.lower() in manifest.description.lower():
                results.append(manifest)
        return results
