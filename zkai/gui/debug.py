"""PySide6 Debug Window Widget."""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit


class DebugWidget(QWidget):
    """Debug Console Window Widget for inspecting system logs and events."""

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.log_view = QTextEdit(self)
        self.log_view.setReadOnly(True)
        layout.addWidget(self.log_view)
