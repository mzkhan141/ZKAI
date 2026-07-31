"""PySide6 Settings Widget."""

from PySide6.QtWidgets import QWidget, QFormLayout, QComboBox, QCheckBox


class SettingsWidget(QWidget):
    """Configuration Settings Panel Widget."""

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QFormLayout(self)

        self.device_combo = QComboBox(self)
        self.device_combo.addItems(["auto", "cuda", "cpu"])
        layout.addRow("Compute Device:", self.device_combo)

        self.reasoning_cb = QCheckBox("Enable Reasoning", self)
        self.reasoning_cb.setChecked(True)
        layout.addRow("Reasoning Engine:", self.reasoning_cb)
