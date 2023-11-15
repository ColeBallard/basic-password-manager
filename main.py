from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QListWidget, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QGuiApplication

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
import base64

import os

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

        self.key = None  # Initialize a variable to store the encryption key

        self.FILE_PATH = 'neddih.txt'

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

        self.text_input = QLineEdit()
        submit_button = self.create_button("Go", lambda: self.submit_input_screen(), 64)

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

        layout.addLayout(self.create_hbox_layout(add_button))
        layout.addWidget(self.search_input)
        layout.addLayout(self.create_hbox_layout(search_button))
        layout.addWidget(self.list_widget)

        self.refresh_list_widget()
        return screen

    def create_add_screen(self):
        screen = QWidget()
        layout = QVBoxLayout(screen)

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

        layout.addWidget(self.error_label)
        layout.addLayout(self.create_hbox_layout(back_button, stretch=True))
        layout.addWidget(self.top_input)
        layout.addLayout(self.create_hbox_layout(add_field_button, remove_field_button, submit_button))
        layout.addWidget(self.bottom_input)

        return screen

    def switch_to_search_screen(self):
        user_input = self.text_input.text()
        self.input_screen.hide()
        self.search_screen.show()
        self.add_screen.hide()

        # Resize the window if necessary
        self.resize(256, 64)

        # Optional: Clear the text input fields on the add screen
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

        # Validate the PIN input
        if pin_input.isdigit() and len(pin_input) == 4:
            self.key = self.derive_key(pin_input)

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
        input_data.append(self.top_input.text())

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
        self.layout.addWidget(self.add_layout.count() - 1, new_input)
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
        # Check if a PIN has been inputted
        if not self.key:
            return
        
        # Read encrypted data from the file
        with open(self.FILE_PATH, 'r') as file:
            encrypted_data = file.read()

        # Check if the file is empty
        if encrypted_data == '':
            return
        
        passwords = [[]]

        # Fill passwords list with decrypted data
        for item in encrypted_data.split(';'):
            print(self.decrypt_data(item.split(':')[0], item.split(':')[1]).split('\n'))
            passwords.append(self.decrypt_data(item.split(':')[0], item.split(':')[1]).split('\n'))

        self.list_widget.clear()

        # Add passwords to list_widget
        for service in passwords:
            i = 0
            for field in service:
                if i == 0:
                    self.list_widget.addItem(field) # Service
                else:
                    self.list_widget.addItem('    ' + field) # Field is indented for clarity

                i += 1

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
        # Implement search functionality here
        pass
        
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

if __name__ == "__main__":
    app = QApplication([])
    window = MyApp()
    window.show()
    app.exec_()
