import os

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QFileDialog

from custom_list import CustomListWidget, CustomListItem
from pcrypt import PCrypt
from screens.input_screen import InputScreen
from screens.search_screen import SearchScreen
from screens.add_screen import AddScreen

class PManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("sdrowssap")
        self.resize(256, 64)

        self.FILE_PATH = 'neddih.txt'

        self.imported = False
        self.imported_data = None

        self.secret_data = {}

        self.pcrypt = PCrypt(None)

        self.init_ui()

    def init_ui(self):
        self.input_screen = InputScreen(self.submit_input_screen, self.import_from_file)
        self.search_screen = SearchScreen(self.switch_to_add_screen, self.search)
        self.add_screen = AddScreen(self.switch_to_search_screen, self.submit_add_screen, self.add_input_field, self.remove_input_field)

        layout = QVBoxLayout(self)
        layout.addWidget(self.input_screen)
        layout.addWidget(self.search_screen)
        layout.addWidget(self.add_screen)

        self.search_screen.hide()
        self.add_screen.hide()

    def switch_to_search_screen(self):
        self.input_screen.hide()
        self.search_screen.show()
        self.add_screen.hide()

        # Resize the window if necessary
        self.resize(512, 512)

        # Clear the text input fields on the add screen
        self.add_screen.top_input.clear()
        self.add_screen.bottom_input.clear()
        for field in self.add_screen.input_fields:
            field.clear()

    def switch_to_add_screen(self):
        self.input_screen.hide()
        self.search_screen.hide()
        self.add_screen.show()

        # Resize the window when switching to the add screen
        self.resize(256, 64)

    def submit_input_screen(self):
        # Retrieve the PIN input from the input_screen instead
        pin_input = self.input_screen.text_input.text()

        self.pcrypt.derive_key(pin_input)         

        if self.imported and len(self.imported_data) > 0:
            self.export_to_file()

        # Refresh the list widget to show the updated data
        self.refresh_list_widget()

        # Switch back to the search screen
        self.switch_to_search_screen()

    def submit_add_screen(self):
        # Check if either top_input or bottom_input is empty
        if not self.add_screen.top_input.text() or not self.add_screen.bottom_input.text():
            self.add_screen.error_label.setText("Top or bottom input cannot be empty.")
            self.add_screen.error_label.show()
            return  # Return early, do not proceed with submission

        # Hide the error label in case it was previously shown
        self.add_screen.error_label.hide()

        # Initialize a list to hold the data from the input fields
        input_data = []

        # Append data from the top permanent input
        input_data.append(self.add_screen.top_input.text().lower())

        # Append data from dynamically added input fields
        for input_field in self.add_screen.input_fields:
            field_data = input_field.text()
            if field_data:
                input_data.append(field_data)

        # Append data from the bottom permanent input
        input_data.append(self.add_screen.bottom_input.text())

        # Append data to file
        self.add_service(input_data)

        # Refresh the list widget to show the updated data
        self.refresh_list_widget()

        # Switch back to the search screen
        self.switch_to_search_screen()

    def add_input_field(self):
        new_input = QLineEdit()
        # Insert the new input field above the bottom input
        self.add_screen.layout.insertWidget(self.add_screen.layout.count() - 1, new_input)
        self.add_screen.input_fields.append(new_input)

    def remove_input_field(self):
        if self.add_screen.input_fields:
            input_to_remove = self.add_screen.input_fields.pop()
            input_to_remove.deleteLater()

    def add_service(self, data):
        # Encrypt the data
        encrypted_data = self.pcrypt.encrypt_data('\n'.join(data))

        # Check if there's any data to append
        if encrypted_data:

            # Opening the file in append mode
            with open(self.FILE_PATH, 'a') as file:

                # Appending the text to the file
                if os.path.getsize(self.FILE_PATH) == 0:
                    file.write(encrypted_data[0] + ':' + encrypted_data[1])  # Adding the first password to the file
                else:
                    file.write(';' + encrypted_data[0] + ':' + encrypted_data[1])  # Adding the remaining passwords to the file

    def refresh_list_widget(self):
        if not self.pcrypt.key:
            return

        # Read encrypted data from the file
        with open(self.FILE_PATH, 'r') as file:
            encrypted_data = file.read()

        if encrypted_data == '':
            return

        # Process and decrypt data into the structured format
        for item in encrypted_data.split(';'):
            service_data = self.pcrypt.decrypt_data(item.split(':')[0], item.split(':')[1]).split('\n')
            service_name = service_data[0]
            self.secret_data[service_name] = service_data[1:]

        self.search_screen.list_widget.clear()

        for service in sorted(self.secret_data.keys()):
            attributes = self.secret_data[service]
            self.search_screen.list_widget.addItem(CustomListItem('service', service))  # Add matching service
            for attr in attributes:
                self.search_screen.list_widget.addItem(CustomListItem('attribute', '    ' + attr))  # Add masked attributes

    def create_button(self, text, function, fixed_width=None):
        button = QPushButton(text)
        if fixed_width:
            button.setFixedWidth(fixed_width)
        button.clicked.connect(function)
        return button

    def search(self):
        search_text = self.search_screen.search_input.text().lower()
        self.search_screen.list_widget.clear()  # Clear current list

        for service in sorted(self.secret_data.keys()):
            if search_text in service.lower():  # Check if search text is in service
                attributes = self.secret_data[service]
                self.search_screen.list_widget.addItem(CustomListItem('service', service))  # Add matching service
                for attr in attributes:
                    self.search_screen.list_widget.addItem(CustomListItem('attribute', '    ' + attr))  # Add masked attributes

    def import_from_file(self):
        # Open file dialog and get the selected file path
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File")
        
        if file_path:  # If a file was selected
            data = {}
            current_service = None

            with open(file_path, 'r') as file:
                for line in file:
                    line = line.strip()  # Remove any leading/trailing whitespace
                    if ' - ' in line:
                        # This line contains a field-attribute pair
                        field, attribute = line.split(' - ', 1)
                        if current_service is not None:
                            data[current_service][field] = attribute
                    else:
                        # This line is a service name
                        current_service = line
                        data[current_service] = {}

                self.imported = True

                self.input_screen.import_label.setText('Choose a master password to access and store all of your passwords.\nPlease write this password down somewhere and don\'t lose it.')

                self.imported_data = data

    def export_to_file(self):
        for outer_key, inner_dict in self.imported_data.items():
            sublist = [outer_key]
            for inner_key, inner_value in inner_dict.items():
                sublist.append(f'{inner_key} : {inner_value}')
            if not(len(sublist) == 1 and sublist[0] == ''):
                self.add_service(sublist)

