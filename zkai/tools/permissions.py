"""PermissionManager for tool approval management."""

from typing import Dict
from zkai.tools.base import Tool, ToolPermission


class PermissionManager:
    """Manages tool execution permission rules."""

    def __init__(self):
        self.permissions: Dict[str, ToolPermission] = {}

    def set_permission(self, tool_name: str, permission: ToolPermission) -> None:
        self.permissions[tool_name] = permission

    def is_allowed(self, tool: Tool) -> bool:
        if tool.metadata.name in self.permissions:
            return self.permissions[tool.metadata.name].allowed
        return tool.permission.allowed
