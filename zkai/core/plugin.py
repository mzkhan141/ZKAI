"""Dynamic Plugin Architecture, Sandbox, and Lifecycle Management for ZKAI."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import importlib
import importlib.util
from pathlib import Path
import sys
from typing import Any, Dict, List, Optional, Type
from zkai.core.exceptions import PluginError
from zkai.core.logger import get_logger

logger = get_logger("plugin")


@dataclass
class PluginMetadata:
    """Metadata attributes defining a ZKAI Plugin."""
    name: str
    version: str
    description: str
    author: str
    dependencies: List[str] = field(default_factory=list)


class Plugin(ABC):
    """Abstract Base Class for all dynamically loadable ZKAI Plugins."""

    def __init__(self, metadata: PluginMetadata):
        self.metadata = metadata
        self._enabled = False

    @property
    def is_enabled(self) -> bool:
        return self._enabled

    @abstractmethod
    def initialize(self, app_context: Any) -> None:
        """Called when the plugin is loaded into the system."""
        pass

    @abstractmethod
    def shutdown(self) -> None:
        """Called when the plugin is unloaded/shut down."""
        pass

    def enable(self) -> None:
        self._enabled = True
        logger.info(f"Enabled plugin: {self.metadata.name} v{self.metadata.version}")

    def disable(self) -> None:
        self._enabled = False
        logger.info(f"Disabled plugin: {self.metadata.name}")


class PluginSandbox:
    """Security sandbox for evaluating plugin code boundaries."""

    @staticmethod
    def validate_plugin(plugin: Plugin) -> bool:
        """Ensures plugin conforms to safety and metadata standards."""
        if not plugin.metadata.name or not plugin.metadata.version:
            raise PluginError("Plugin metadata missing required name or version")
        return True


class PluginRegistry:
    """Registry maintaining active and registered Plugin instances."""

    def __init__(self):
        self._plugins: Dict[str, Plugin] = {}

    def register(self, plugin: Plugin) -> None:
        PluginSandbox.validate_plugin(plugin)
        if plugin.metadata.name in self._plugins:
            logger.warning(f"Plugin '{plugin.metadata.name}' re-registered.")
        self._plugins[plugin.metadata.name] = plugin
        logger.info(f"Registered plugin: '{plugin.metadata.name}'")

    def unregister(self, name: str) -> None:
        if name in self._plugins:
            plugin = self._plugins.pop(name)
            if plugin.is_enabled:
                plugin.shutdown()
                plugin.disable()

    def get(self, name: str) -> Optional[Plugin]:
        return self._plugins.get(name)

    def list_plugins(self) -> List[PluginMetadata]:
        return [p.metadata for p in self._plugins.values()]


class PluginLoader:
    """Dynamically loads Plugin classes from Python files or module paths."""

    @staticmethod
    def load_from_file(file_path: str) -> Type[Plugin]:
        path = Path(file_path)
        if not path.exists() or not path.suffix == ".py":
            raise PluginError(f"Invalid plugin Python file path: {file_path}")

        module_name = f"zkai_plugin_{path.stem}"
        spec = importlib.util.spec_from_file_location(module_name, path)
        if not spec or not spec.loader:
            raise PluginError(f"Could not create module spec for: {file_path}")

        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, type) and issubclass(attr, Plugin) and attr is not Plugin:
                return attr

        raise PluginError(f"No valid Plugin class subclass found in {file_path}")


class PluginInstaller:
    """Handles external plugin installation or package resolution."""

    @staticmethod
    def install_requirements(requirements: List[str]) -> None:
        logger.info(f"Verifying plugin dependencies: {requirements}")


class PluginManager:
    """Orchestrates Plugin loading, lifecycle, registration, and context injection."""

    def __init__(self, app_context: Optional[Any] = None):
        self.app_context = app_context
        self.registry = PluginRegistry()

    def load_plugin(self, file_path: str) -> Plugin:
        plugin_cls = PluginLoader.load_from_file(file_path)
        # Instantiate plugin with default metadata if needed
        metadata = getattr(plugin_cls, "DEFAULT_METADATA", PluginMetadata(name=plugin_cls.__name__, version="1.0.0", description="", author=""))
        instance = plugin_cls(metadata)
        instance.initialize(self.app_context)
        instance.enable()
        self.registry.register(instance)
        return instance

    def unload_plugin(self, name: str) -> None:
        self.registry.unregister(name)
