"""PySide6 Tool Inspector Widget."""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem


class ToolInspectorWidget(QWidget):
    """Tool Inspector Widget for inspecting registered tool capabilities and parameters."""

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.tree = QTreeWidget(self)
        self.tree.setHeaderLabels(["Tool Name", "Description", "Category"])
        layout.addWidget(self.tree)
