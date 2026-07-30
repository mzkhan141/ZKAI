"""PySide6 Conversation History Widget."""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget


class HistoryWidget(QWidget):
    """Conversation History Navigation Widget."""

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.history_list = QListWidget(self)
        layout.addWidget(self.history_list)
