# File: components/service_item_widget.py
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout

class ServiceItemWidget(QWidget):
    def __init__(self, service_name, on_edit_callback):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 2, 5, 2)

        self.label = QLabel(service_name)
        self.edit_button = QPushButton("Edit")
        self.edit_button.setFixedWidth(50)
        self.edit_button.clicked.connect(lambda: on_edit_callback(service_name))

        layout.addWidget(self.label)
        layout.addStretch()
        layout.addWidget(self.edit_button)