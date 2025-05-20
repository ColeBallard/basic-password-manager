import os
import time
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QFileDialog, QMessageBox
from widgets.custom_list import CustomListWidget
from widgets.custom_layouts import create_hbox_layout

class SearchScreen(QWidget):
    def __init__(self, add_callback, search_callback):
        super().__init__()
        layout = QVBoxLayout(self)

        utilities_buttons = QHBoxLayout()
        add_button = QPushButton("Add Service")
        add_button.setFixedWidth(80)
        add_button.clicked.connect(add_callback)
        utilities_buttons.addWidget(add_button)

        append_button = QPushButton("Append File")
        append_button.setFixedWidth(80)
        append_button.clicked.connect(self.append_encrypted_file)
        utilities_buttons.addWidget(append_button)

        self.search_input = QLineEdit()
        self.search_input.returnPressed.connect(search_callback)

        search_button = QPushButton("Search")
        search_button.setFixedWidth(64)
        search_button.clicked.connect(search_callback)

        self.list_widget = CustomListWidget()

        layout.addLayout(utilities_buttons)
        layout.addWidget(self.search_input)
        layout.addLayout(create_hbox_layout(search_button))
        layout.addWidget(self.list_widget)

    def append_encrypted_file(self):
        QMessageBox.information(
            self,
            "Important Notice",
            "To append a file, both files must be encrypted using the same master password.\n"
            "Please ensure compatibility before continuing.",
            QMessageBox.Ok
        )

        # Step 1: Choose the file to merge
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Encrypted File to Append",
            "",
            "Text Files (*.txt);;All Files (*)"
        )

        if not file_path or not os.path.exists(file_path):
            return

        # Step 2: Read lines from current file and selected file
        try:
            with open(self.window().FILE_PATH, 'r') as f:
                original_lines = set(line.strip() for line in f if line.strip())

            with open(file_path, 'r') as f:
                new_lines = set(line.strip() for line in f if line.strip())

            combined_lines = original_lines.union(new_lines)

            # Step 3: Backup current file with timestamp
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            backup_path = f"{self.window().FILE_PATH}_backup_{timestamp}.txt"
            with open(backup_path, 'w') as backup_file:
                backup_file.write('\n'.join(sorted(original_lines)) + '\n')

            # Step 4: Write new combined data to FILE_PATH
            with open(self.window().FILE_PATH, 'w') as target_file:
                target_file.write('\n'.join(sorted(combined_lines)) + '\n')

            QMessageBox.information(self, "Success", f"File appended and backed up as:\n{os.path.basename(backup_path)}")

            self.window().refresh_list_widget()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred:\n{str(e)}")
