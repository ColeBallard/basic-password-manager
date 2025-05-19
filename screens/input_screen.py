from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from widgets.custom_layouts import create_hbox_layout

class InputScreen(QWidget):
    def __init__(self, submit_callback, import_callback):
        super().__init__()
        layout = QVBoxLayout(self)

        import_button = QPushButton('Import')
        import_button.setFixedWidth(64)
        import_button.clicked.connect(import_callback)

        self.import_label = QLabel('')
        self.text_input = QLineEdit()
        self.text_input.setEchoMode(QLineEdit.Password)

        submit_button = QPushButton("Go")
        submit_button.setFixedWidth(64)
        submit_button.clicked.connect(submit_callback)

        self.text_input.returnPressed.connect(submit_callback)

        layout.addLayout(create_hbox_layout(import_button))
        layout.addWidget(self.import_label)
        layout.addWidget(self.text_input)
        layout.addLayout(create_hbox_layout(submit_button))
