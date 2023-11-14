from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QListWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QGuiApplication

class CustomListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if event.button() == Qt.LeftButton:
            self.copy_field_to_clipboard()

    def copy_field_to_clipboard(self):
        item = self.currentItem()
        if item and ':' in item.text():
            clipboard = QGuiApplication.clipboard()
            field_text = item.text().split(':', 1)[1].strip()
            clipboard.setText(field_text)

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("sdrowssap")
        self.resize(256, 64)

        # Initialize the screens
        self.init_input_screen()
        self.init_search_screen()
        self.init_add_screen()

        # Main layout
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.input_screen)
        self.layout.addWidget(self.search_screen)
        self.layout.addWidget(self.add_screen)

        

        # Initially hide the search and add screens
        self.search_screen.hide()
        self.add_screen.hide()

    def init_input_screen(self):
        self.input_screen = QWidget()
        layout = QVBoxLayout(self.input_screen)

        self.text_input = QLineEdit()
        layout.addWidget(self.text_input)

        button_layout = QHBoxLayout()
        button_layout.addStretch(1)

        submit_button = QPushButton("Go")
        submit_button.setFixedWidth(64)
        submit_button.clicked.connect(self.switch_to_search_screen)
        button_layout.addWidget(submit_button)
        button_layout.addStretch(1)

        layout.addLayout(button_layout)

    def init_search_screen(self):
        self.search_screen = QWidget()
        layout = QVBoxLayout(self.search_screen)

        top_layout = QHBoxLayout()
        top_layout.addStretch(1)

        add_button = QPushButton("Add")
        add_button.clicked.connect(self.switch_to_add_screen)
        top_layout.addWidget(add_button)

        layout.addLayout(top_layout)

        self.search_input = QLineEdit()
        layout.addWidget(self.search_input)

        search_button_layout = QHBoxLayout()
        search_button_layout.addStretch(1)

        search_button = QPushButton("Search")
        search_button.setFixedWidth(64)
        search_button.clicked.connect(self.search)
        search_button_layout.addWidget(search_button)
        search_button_layout.addStretch(1)

        layout.addLayout(search_button_layout)

        list_widget = CustomListWidget()

        layout.addWidget(list_widget)

        # Assuming the file path is known
        file_path = "neddih.txt"
        raw_data = self.read_from_file(file_path)
        structured_data = self.decipher_data(raw_data)
        self.update_list_widget(list_widget, structured_data)

    def init_add_screen(self):
        self.add_screen = QWidget()
        self.add_layout = QVBoxLayout(self.add_screen)

        # Top layout for the Back button
        top_layout = QHBoxLayout()
        back_button = QPushButton("<-")
        back_button.setMinimumWidth(40)  # Set minimum width
        back_button.setMaximumWidth(40) # Set maximum width
        back_button.clicked.connect(self.switch_to_search_screen)
        top_layout.addWidget(back_button)
        top_layout.addStretch(1)
        self.add_layout.addLayout(top_layout)

        # Permanent top text input
        self.top_input = QLineEdit()
        self.add_layout.addWidget(self.top_input)

        # Horizontal layout for the other buttons
        buttons_layout = QHBoxLayout()

        add_field_button = QPushButton("+")
        add_field_button.setMinimumWidth(40)  # Set minimum width
        add_field_button.clicked.connect(self.add_input_field)
        buttons_layout.addWidget(add_field_button)

        remove_field_button = QPushButton("-")
        remove_field_button.setMinimumWidth(40)  # Set minimum width
        remove_field_button.clicked.connect(self.remove_input_field)
        buttons_layout.addWidget(remove_field_button)

        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.submit_add_screen)
        buttons_layout.addWidget(submit_button)

        self.add_layout.addLayout(buttons_layout)

        # Permanent bottom text input
        self.bottom_input = QLineEdit()
        self.add_layout.addWidget(self.bottom_input)

        # List to keep track of dynamically added input fields
        self.input_fields = []

    def submit_add_screen(self):
        # Here, you can implement what happens when the submit button is clicked.
        # For example, gather the data from the input fields and process it.
        pass

    def add_input_field(self):
        new_input = QLineEdit()
        # Insert the new input field above the bottom input
        self.add_layout.insertWidget(self.add_layout.count() - 1, new_input)
        self.input_fields.append(new_input)

    def remove_input_field(self):
        if self.input_fields:
            input_to_remove = self.input_fields.pop()
            input_to_remove.deleteLater()

    def switch_to_search_screen(self):
        user_input = self.text_input.text()
        self.input_screen.hide()
        self.search_screen.show()
        self.add_screen.hide()

    def switch_to_add_screen(self):
        self.input_screen.hide()
        self.search_screen.hide()
        self.add_screen.show()

        # Resize the window when switching to the add screen
        self.resize(256, 64)

    def search(self):
        # Implement search functionality here
        pass

    def read_from_file(self, file_path):
        with open(file_path, 'r') as file:
            return file.readlines()
        
    def update_list_widget(self, list_widget, structured_data):
        list_widget.clear()
        last_item = None
        
        for item, field in structured_data:
            if item != last_item:
                list_widget.addItem(item)  # Add the main item
                last_item = item
            list_widget.addItem(f"  {field}")  # Add the field, indented for clarity
        
    def decipher_data(self, data):
        print(data)
        structured_data = []
        current_item = None

        for line in data:
            line = line.strip()
            if line:  # Check if line is not empty
                if current_item is None:
                    current_item = line
                else:
                    structured_data.append((current_item, line))
            else:
                current_item = None  # Reset for the next item
        return structured_data
    
if __name__ == "__main__":
    app = QApplication([])
    window = MyApp()
    window.show()
    app.exec_()
