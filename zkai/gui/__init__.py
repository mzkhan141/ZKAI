"""PySide6 Desktop Studio GUI for ZKAI."""

from zkai.gui.app import ZKAIApp, ZKAIMainWindow
from zkai.gui.chat import ChatWidget
from zkai.gui.settings import SettingsWidget
from zkai.gui.history import HistoryWidget
from zkai.gui.debug import DebugWidget
from zkai.gui.tool_inspector import ToolInspectorWidget
from zkai.gui.memory_viewer import MemoryViewerWidget

__all__ = [
    "ZKAIApp",
    "ZKAIMainWindow",
    "ChatWidget",
    "SettingsWidget",
    "HistoryWidget",
    "DebugWidget",
    "ToolInspectorWidget",
    "MemoryViewerWidget",
]
