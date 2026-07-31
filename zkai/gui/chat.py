"""PySide6 Chat Interface Widget."""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton


class ChatWidget(QWidget):
    """Chat Interface Widget with conversation history and input box."""

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        self.chat_history = QTextEdit(self)
        self.chat_history.setReadOnly(True)
        layout.addWidget(self.chat_history)

        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Type your message here...")
        layout.addWidget(self.input_field)

        self.send_button = QPushButton("Send", self)
        layout.addWidget(self.send_button)
