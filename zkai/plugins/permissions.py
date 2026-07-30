"""PluginPermission and PermissionChecker."""

from dataclasses import dataclass
from typing import List, Optional, Set


@dataclass
class PluginPermission:
    name: str
    granted: bool = False


class PluginPermissionChecker:
    """Verifies requested plugin permissions against user-granted capabilities."""

    def __init__(self, allowed_permissions: Optional[List[str]] = None):
        self.allowed_permissions: Set[str] = set(allowed_permissions or ["read_file", "network"])

    def verify_permissions(self, requested: List[str]) -> bool:
        for p in requested:
            if p not in self.allowed_permissions:
                return False
        return True
