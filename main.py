from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QListWidget, QListWidgetItem, QLabel, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
import base64

import os

class CustomListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            item = self.currentItem()
            if item and isinstance(item, CustomListItem) and item.type == 'attribute':
                QApplication.clipboard().setText(item.getActualValue())
                QMessageBox.information(self, "Copied", "Value copied to clipboard.")

class CustomListItem(QListWidgetItem):
    def __init__(self, type, text, parent=None):
        super().__init__(parent)
        self.type = type  # 'service' or 'attribute'
        self.full_text = text
        self.actual_value = ""

        if type == 'attribute':
            attr, value = text.split(':')
            self.actual_value = value.strip()
            masked_value = '*' * len(self.actual_value)
            self.setText(f"{attr}: {masked_value}")
        else:
            self.setText(text)

    def getActualValue(self):
        return self.actual_value

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("sdrowssap")
        self.resize(256, 64)

        self.key = None  # Initialize a variable to store the encryption key

        self.FILE_PATH = 'neddih.txt'

        self.imported = False
        self.imported_data = None

        self.secret_data = {}

        self.init_ui()

    def init_ui(self):
        # Main layout
        self.layout = QVBoxLayout(self)

        # Initialize the screens
        self.input_screen = self.create_input_screen()
        self.search_screen = self.create_search_screen()
        self.add_screen = self.create_add_screen()

        # Add screens to layout and hide optional screens initially
        self.layout.addWidget(self.input_screen)
        self.layout.addWidget(self.search_screen)
        self.layout.addWidget(self.add_screen)
        self.search_screen.hide()
        self.add_screen.hide()

    def create_input_screen(self):
        screen = QWidget()
        layout = QVBoxLayout(screen)

        import_button = QPushButton('Import')
        import_button.setFixedWidth(64)
        import_button.clicked.connect(self.import_from_file)
        self.import_label = QLabel('')

        self.text_input = QLineEdit()
        self.text_input.setEchoMode(QLineEdit.Password)
        submit_button = self.create_button("Go", self.submit_input_screen, 64)

        self.text_input.returnPressed.connect(self.submit_input_screen)

        layout.addLayout(self.create_hbox_layout(import_button))
        layout.addWidget(self.import_label)
        layout.addWidget(self.text_input)
        layout.addLayout(self.create_hbox_layout(submit_button))
        return screen

    def create_search_screen(self):
        screen = QWidget()
        layout = QVBoxLayout(screen)

        add_button = self.create_button("Add", self.switch_to_add_screen, 64)
        self.search_input = QLineEdit()
        search_button = self.create_button("Search", self.search, 64)
        self.list_widget = CustomListWidget()

        self.search_input.returnPressed.connect(self.search)

        layout.addLayout(self.create_hbox_layout(add_button))
        layout.addWidget(self.search_input)
        layout.addLayout(self.create_hbox_layout(search_button))
        layout.addWidget(self.list_widget)

        self.refresh_list_widget()
        return screen

    def create_add_screen(self):
        screen = QWidget()
        self.add_screen_layout = QVBoxLayout(screen)

        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: red;")
        self.error_label.hide()

        back_button = self.create_button("<-", self.switch_to_search_screen, 40)
        self.top_input = QLineEdit()
        add_field_button = self.create_button("+", self.add_input_field, 40)
        remove_field_button = self.create_button("-", self.remove_input_field, 40)
        submit_button = self.create_button("Submit", self.submit_add_screen)
        self.bottom_input = QLineEdit()
        self.input_fields = []

        self.add_screen_layout.addWidget(self.error_label)
        self.add_screen_layout.addLayout(self.create_hbox_layout(back_button, stretch=True))
        self.add_screen_layout.addWidget(self.top_input)
        self.add_screen_layout.addLayout(self.create_hbox_layout(add_field_button, remove_field_button, submit_button))
        self.add_screen_layout.addWidget(self.bottom_input)

        return screen

    def switch_to_search_screen(self):
        self.input_screen.hide()
        self.search_screen.show()
        self.add_screen.hide()

        # Resize the window if necessary
        self.resize(512, 512)

        # Clear the text input fields on the add screen
        self.top_input.clear()
        self.bottom_input.clear()
        for field in self.input_fields:
            field.clear()

    def switch_to_add_screen(self):
        self.input_screen.hide()
        self.search_screen.hide()
        self.add_screen.show()

        # Resize the window when switching to the add screen
        self.resize(256, 64)

    def submit_input_screen(self):
        # Retrieve the PIN input
        pin_input = self.text_input.text()

        self.key = self.derive_key(pin_input)         

        if self.imported and len(self.imported_data) > 0:
            self.export_to_file()

        # Refresh the list widget to show the updated data
        self.refresh_list_widget()

        # Switch back to the search screen
        self.switch_to_search_screen()

    def submit_add_screen(self):
        # Check if either top_input or bottom_input is empty
        if not self.top_input.text() or not self.bottom_input.text():
            self.error_label.setText("Top or bottom input cannot be empty.")
            self.error_label.show()
            return  # Return early, do not proceed with submission

        # Hide the error label in case it was previously shown
        self.error_label.hide()

        # Initialize a list to hold the data from the input fields
        input_data = []

        # Append data from the top permanent input
        input_data.append(self.top_input.text().lower())

        # Append data from dynamically added input fields
        for input_field in self.input_fields:
            field_data = input_field.text()
            if field_data:
                input_data.append(field_data)

        # Append data from the bottom permanent input
        input_data.append(self.bottom_input.text())

        # Append data to file
        self.add_service(input_data)

        # Refresh the list widget to show the updated data
        self.refresh_list_widget()

        # Switch back to the search screen
        self.switch_to_search_screen()

    def add_input_field(self):
        new_input = QLineEdit()
        # Insert the new input field above the bottom input
        self.add_screen_layout.insertWidget(self.add_screen_layout.count() - 1, new_input)
        self.input_fields.append(new_input)

    def remove_input_field(self):
        if self.input_fields:
            input_to_remove = self.input_fields.pop()
            input_to_remove.deleteLater()

    def add_service(self, data):
        # Encrypt the data
        encrypted_data = self.encrypt_data('\n'.join(data))

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
        if not self.key:
            return

        # Read encrypted data from the file
        with open(self.FILE_PATH, 'r') as file:
            encrypted_data = file.read()

        if encrypted_data == '':
            return

        # Process and decrypt data into the structured format
        for item in encrypted_data.split(';'):
            service_data = self.decrypt_data(item.split(':')[0], item.split(':')[1]).split('\n')
            service_name = service_data[0]
            self.secret_data[service_name] = service_data[1:]

        self.list_widget.clear()

        for service in sorted(self.secret_data.keys()):
            attributes = self.secret_data[service]
            self.list_widget.addItem(CustomListItem('service', service))  # Add matching service
            for attr in attributes:
                self.list_widget.addItem(CustomListItem('attribute', '    ' + attr))  # Add masked attributes

    def create_button(self, text, function, fixed_width=None):
        button = QPushButton(text)
        if fixed_width:
            button.setFixedWidth(fixed_width)
        button.clicked.connect(function)
        return button

    def create_hbox_layout(self, *widgets, stretch=False):
        layout = QHBoxLayout()
        if stretch:
            layout.addStretch(1)
        for widget in widgets:
            layout.addWidget(widget)
        if stretch:
            layout.addStretch(1)
        return layout

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

    def search(self):
        search_text = self.search_input.text().lower()
        self.list_widget.clear()  # Clear current list

        for service in sorted(self.secret_data.keys()):
            if search_text in service.lower():  # Check if search text is in service
                attributes = self.secret_data[service]
                self.list_widget.addItem(CustomListItem('service', service))  # Add matching service
                for attr in attributes:
                    self.list_widget.addItem(CustomListItem('attribute', '    ' + attr))  # Add masked attributes

    def derive_key(self, pin):
        # Derive a 256-bit key using the provided pin
        salt = b'\x00'*16  # Static salt; in a real-world scenario, use a random salt
        key = PBKDF2(pin, salt, dkLen=32, count=1000000)
        return key

    def encrypt_data(self, data):
        if self.key == None:
            return data

        # Prepare data for encryption (AES requires 16-byte blocks)
        data = data.encode('utf-8')
        pad = 16 - len(data) % 16
        data += bytes([pad] * pad)

        # Encrypt data
        cipher = AES.new(self.key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(data)
        iv = cipher.iv

        # Encode the encrypted data and IV to base64
        iv = base64.b64encode(iv).decode('utf-8')
        ct = base64.b64encode(ct_bytes).decode('utf-8')
        return iv, ct

    def decrypt_data(self, iv, ct):
        # Decode the base64 encoded iv and encrypted data
        iv = base64.b64decode(iv)
        ct = base64.b64decode(ct)

        # Decrypt the data
        cipher = AES.new(self.key, AES.MODE_CBC, iv=iv)
        pt = cipher.decrypt(ct)

        # Remove padding
        pad = pt[-1]
        pt = pt[:-pad]

        return pt.decode('utf-8')

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

                self.import_label.setText('Choose a master password to access and store all of your passwords.\nPlease write this password down somewhere and don\'t lose it.')

                self.imported_data = data

    def export_to_file(self):
        for outer_key, inner_dict in self.imported_data.items():
            sublist = [outer_key]
            for inner_key, inner_value in inner_dict.items():
                sublist.append(f'{inner_key} : {inner_value}')
            if not(len(sublist) == 1 and sublist[0] == ''):
                self.add_service(sublist)

if __name__ == "__main__":
    app = QApplication([])
    window = MyApp()
    window.show()
    app.exec_()
