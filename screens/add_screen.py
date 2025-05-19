from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
from widgets.custom_layouts import create_hbox_layout

class AddScreen(QWidget):
    def __init__(self, back_callback, submit_callback, add_field_callback, remove_field_callback):
        super().__init__()
        self.layout = QVBoxLayout(self)

        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: red;")
        self.error_label.hide()

        back_button = QPushButton("<-")
        back_button.setFixedWidth(40)
        back_button.clicked.connect(back_callback)

        self.top_input = QLineEdit()
        self.bottom_input = QLineEdit()

        add_button = QPushButton("+")
        add_button.setFixedWidth(40)
        add_button.clicked.connect(add_field_callback)

        remove_button = QPushButton("-")
        remove_button.setFixedWidth(40)
        remove_button.clicked.connect(remove_field_callback)

        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(submit_callback)

        self.input_fields = []

        self.layout.addWidget(self.error_label)
        self.layout.addLayout(create_hbox_layout(back_button, stretch=True))
        self.layout.addWidget(self.top_input)
        self.layout.addLayout(create_hbox_layout(add_button, remove_button, submit_button))
        self.layout.addWidget(self.bottom_input)
