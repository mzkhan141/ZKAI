"""PySide6 Memory Viewer Widget."""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem


class MemoryViewerWidget(QWidget):
    """Memory Viewer Widget for inspecting active working, short-term, and long-term memory entries."""

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.table = QTableWidget(0, 3, self)
        self.table.setHorizontalHeaderLabels(["Memory Key", "Type", "Content"])
        layout.addWidget(self.table)
