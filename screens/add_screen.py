from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
from widgets.custom_layouts import create_hbox_layout
from components.attribute_value_input import AttributeValueInput

class AddScreen(QWidget):
    def __init__(self, back_callback, submit_callback):
        super().__init__()
        self.layout = QVBoxLayout(self)

        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: red;")
        self.error_label.hide()

        back_button = QPushButton("Back")
        back_button.setFixedWidth(40)
        back_button.clicked.connect(back_callback)

        self.service_name_input = QLineEdit()
        self.service_name_input.setPlaceholderText("Service Name")

        attribute_value_input = AttributeValueInput()

        add_button = QPushButton("Add Field")
        add_button.setFixedWidth(80)
        add_button.clicked.connect(self.add_input_field)

        remove_button = QPushButton("Remove Field")
        remove_button.setFixedWidth(80)
        remove_button.clicked.connect(self.remove_input_field)

        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(submit_callback)

        self.layout.addWidget(self.error_label)
        self.layout.addLayout(create_hbox_layout(back_button, stretch=True))
        self.layout.addWidget(self.service_name_input)
        self.layout.addLayout(create_hbox_layout(add_button, remove_button, submit_button))
        self.layout.addWidget(attribute_value_input)

        self.input_fields = [attribute_value_input]

    def add_input_field(self):
        new_input = AttributeValueInput()
        # Insert the new input field below the bottom input
        self.layout.addWidget(new_input)
        self.input_fields.append(new_input)

    def remove_input_field(self):
        if len(self.input_fields) > 1:
            input_to_remove = self.input_fields.pop()
            input_to_remove.setParent(None)
            input_to_remove.deleteLater()

            self.layout.invalidate()
            self.window().adjustSize()
        else:
            self.error_label.setText("Cannot remove last field.")
            self.error_label.show()
        
    def clear_fields(self):
        self.service_name_input.clear()

        # Keep the first field, remove the rest
        while len(self.input_fields) > 1:
            field_to_remove = self.input_fields.pop()
            field_to_remove.setParent(None)
            field_to_remove.deleteLater()

        # Clear the one remaining field
        self.input_fields[0].clear()

        self.error_label.hide()
        self.layout.invalidate()
        self.window().adjustSize()
