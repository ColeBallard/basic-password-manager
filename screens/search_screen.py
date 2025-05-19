from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton
from custom_list import CustomListWidget
from widgets.custom_layouts import create_hbox_layout

class SearchScreen(QWidget):
    def __init__(self, add_callback, search_callback):
        super().__init__()
        layout = QVBoxLayout(self)

        add_button = QPushButton("Add")
        add_button.setFixedWidth(64)
        add_button.clicked.connect(add_callback)

        self.search_input = QLineEdit()
        self.search_input.returnPressed.connect(search_callback)

        search_button = QPushButton("Search")
        search_button.setFixedWidth(64)
        search_button.clicked.connect(search_callback)

        self.list_widget = CustomListWidget()

        layout.addLayout(create_hbox_layout(add_button))
        layout.addWidget(self.search_input)
        layout.addLayout(create_hbox_layout(search_button))
        layout.addWidget(self.list_widget)
