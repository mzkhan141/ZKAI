"""DependencyResolver for plugin loading order and topological sort."""

from typing import Dict, List, Set
from zkai.core.exceptions import PluginError
from zkai.plugins.manifest import PluginManifest


class DependencyResolver:
    """Resolves plugin dependencies and determines valid load order."""

    @staticmethod
    def resolve_load_order(manifests: List[PluginManifest]) -> List[PluginManifest]:
        manifest_map: Dict[str, PluginManifest] = {m.name: m for m in manifests}
        graph: Dict[str, Set[str]] = {m.name: set(m.dependencies) for m in manifests}
        ordered: List[PluginManifest] = []
        visited: Set[str] = set()
        visiting: Set[str] = set()

        def dfs(node: str) -> None:
            if node in visiting:
                raise PluginError(f"Circular dependency detected in plugin: {node}")
            if node not in visited:
                visiting.add(node)
                for dep in graph.get(node, []):
                    if dep in manifest_map:
                        dfs(dep)
                    else:
                        raise PluginError(f"Missing required dependency '{dep}' for plugin '{node}'")
                visiting.remove(node)
                visited.add(node)
                if node in manifest_map:
                    ordered.append(manifest_map[node])

        for m in manifests:
            if m.name not in visited:
                dfs(m.name)

        return ordered
