import os

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, QListWidgetItem
from PyQt5.QtCore import QTimer

from widgets.custom_list import CustomListWidget, CustomListItem
from widgets.service_item_widget import ServiceItemWidget
from components.attribute_value_input import AttributeValueInput
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
        self.editing_service = None

        self.pcrypt = PCrypt(None)

        self.init_ui()

    def init_ui(self):
        self.input_screen = InputScreen(self.submit_input_screen, self.import_from_file)
        self.search_screen = SearchScreen(self.switch_to_add_screen, self.search)
        self.add_screen = AddScreen(self.switch_to_search_screen, self.submit_add_screen)

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

        self.adjustSize()

        # Clear the text input fields on the add screen
        self.add_screen.clear_fields()

        # Add a small delay to let the list widget calculate its contents
        QTimer.singleShot(100, self.adjust_window_width)

    def adjust_window_width(self):
        # Calculate the width needed for the list widget
        list_width = self.search_screen.list_widget.sizeHintForColumn(0) + 80  # Add padding
        
        # Get the current window size
        current_size = self.size()
        
        # Set a minimum width (prevents too narrow windows)
        min_width = max(300, list_width)
        
        # Resize the window with the new width but keep the current height
        self.resize(min_width, current_size.height())

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
        # Initialize a list to hold the data from the input fields
        input_data = []

        if not self.add_screen.service_name_input.text():
            self.add_screen.error_label.setText("Service name cannot be empty.")
            self.add_screen.error_label.show()
            return  # Return early, do not proceed with submission
        else:
            input_data.append(self.add_screen.service_name_input.text().lower())
        
        # Hide the error label in case it was previously shown
        self.add_screen.error_label.hide()

        for field in self.add_screen.input_fields:
            if not field.has_text():
                self.add_screen.error_label.setText("Cannot have empty fields.")
                self.add_screen.error_label.show()
                return  # Return early, do not proceed with submission
            else:
                input_data.append(field.get_text())

        # Hide the error label in case it was previously shown
        self.add_screen.error_label.hide()

        # If we're editing an existing service, remove the old one first
        if hasattr(self, 'editing_service') and self.editing_service:
            del self.secret_data[self.editing_service]
            self.write_all_services()  # Save current data minus the old one
            self.editing_service = None

        # Append data to file
        self.add_service(input_data)

        # Refresh the list widget to show the updated data
        self.refresh_list_widget()

        # Switch back to the search screen
        self.switch_to_search_screen()

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

    def edit_service(self, service_name):
        self.editing_service = service_name
        self.switch_to_add_screen()

        # Prefill service name
        self.add_screen.service_name_input.setText(service_name)

        # Clear current input fields
        for field in self.add_screen.input_fields:
            field.setParent(None)
        self.add_screen.input_fields.clear()

        # Add inputs for each field
        for attr in self.secret_data[service_name]:
            attr_val = attr.split(':', 1)
            input_widget = AttributeValueInput()
            if len(attr_val) == 2:
                input_widget.attribute_input.setText(attr_val[0].strip())
                input_widget.value_input.setText(attr_val[1].strip())
            self.add_screen.layout.addWidget(input_widget)
            self.add_screen.input_fields.append(input_widget)

    def custom_key(self, char):
        return (char.upper(), 0 if char.isupper() else 1)

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

        for service in sorted(self.secret_data.keys(), key=self.custom_key):
            attributes = self.secret_data[service]

            # Inside refresh_list_widget()
            item_widget = ServiceItemWidget(service, self.edit_service)
            list_item = QListWidgetItem()
            list_item.setSizeHint(item_widget.sizeHint())

            self.search_screen.list_widget.addItem(list_item)
            self.search_screen.list_widget.setItemWidget(list_item, item_widget)
            # Add matching service
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

        for service in sorted(self.secret_data.keys(), key=self.custom_key):
            if search_text in service.lower():  # Check if search text is in service
                attributes = self.secret_data[service]
                item_widget = ServiceItemWidget(service, self.edit_service)
                list_item = QListWidgetItem()
                list_item.setSizeHint(item_widget.sizeHint())

                self.search_screen.list_widget.addItem(list_item)
                self.search_screen.list_widget.setItemWidget(list_item, item_widget)
                for attr in attributes:
                    self.search_screen.list_widget.addItem(CustomListItem('attribute', '    ' + attr))  # Add masked attributes

    def write_all_services(self):
        with open(self.FILE_PATH, 'w') as file:
            all_entries = []
            for service, attributes in self.secret_data.items():
                plain = '\n'.join([service] + attributes)
                enc = self.pcrypt.encrypt_data(plain)
                all_entries.append(enc[0] + ':' + enc[1])
            file.write(';'.join(all_entries))

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

