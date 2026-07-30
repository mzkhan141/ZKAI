"""Main Desktop GUI Application powered by PySide6."""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget
from zkai.gui.chat import ChatWidget
from zkai.gui.settings import SettingsWidget
from zkai.gui.history import HistoryWidget
from zkai.gui.debug import DebugWidget
from zkai.gui.tool_inspector import ToolInspectorWidget
from zkai.gui.memory_viewer import MemoryViewerWidget
from zkai.core.logger import get_logger

logger = get_logger("gui.app")


class ZKAIMainWindow(QMainWindow):
    """Main Application Window for ZKAI Desktop GUI."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("ZKAI — AI Operating System Desktop Studio")
        self.resize(1100, 750)

        self.tabs = QTabWidget(self)
        self.setCentralWidget(self.tabs)

        self.chat_widget = ChatWidget(self)
        self.settings_widget = SettingsWidget(self)
        self.history_widget = HistoryWidget(self)
        self.debug_widget = DebugWidget(self)
        self.tool_inspector = ToolInspectorWidget(self)
        self.memory_viewer = MemoryViewerWidget(self)

        self.tabs.addTab(self.chat_widget, "Chat Studio")
        self.tabs.addTab(self.memory_viewer, "Memory Viewer")
        self.tabs.addTab(self.tool_inspector, "Tool Inspector")
        self.tabs.addTab(self.history_widget, "History")
        self.tabs.addTab(self.debug_widget, "Debug Console")
        self.tabs.addTab(self.settings_widget, "Settings")


class ZKAIApp:
    """Desktop Application launcher."""

    def launch(self) -> None:
        logger.info("Launching ZKAI PySide6 Desktop GUI...")
        app = QApplication.instance() or QApplication(sys.argv)
        window = ZKAIMainWindow()
        window.show()
        app.exec()
