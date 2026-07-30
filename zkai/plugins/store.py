"""PluginStore for discovery and local plugin management."""

from pathlib import Path
from typing import Dict, List, Optional
from zkai.plugins.manifest import PluginManifest


class PluginStore:
    """Manages local plugin repository directory and available plugin manifests."""

    def __init__(self, plugins_dir: str = "./zkai_plugins"):
        self.plugins_dir = Path(plugins_dir)
        self.plugins_dir.mkdir(parents=True, exist_ok=True)

    def discover_plugins(self) -> List[PluginManifest]:
        manifests: List[PluginManifest] = []
        for p in self.plugins_dir.glob("*/manifest.json"):
            manifests.append(PluginManifest.from_file(str(p)))
        for p in self.plugins_dir.glob("*/manifest.yaml"):
            manifests.append(PluginManifest.from_file(str(p)))
        return manifests

    def get_plugin_path(self, plugin_name: str) -> Optional[Path]:
        for d in self.plugins_dir.iterdir():
            if d.is_dir() and d.name == plugin_name:
                return d
        return None
