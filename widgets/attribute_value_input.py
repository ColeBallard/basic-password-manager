from PyQt5.QtWidgets import QWidget, QLineEdit, QHBoxLayout, QSizePolicy

class AttributeValueInput(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.attribute_input = QLineEdit()
        self.attribute_input.setPlaceholderText("Attribute")

        self.value_input = QLineEdit()
        self.value_input.setPlaceholderText("Value")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        
        layout.addWidget(self.attribute_input)
        layout.addWidget(self.value_input)

    def has_text(self):
        return self.attribute_input.text() and self.value_input.text()
    
    def get_text(self):
        return f"{self.attribute_input.text()} : {self.value_input.text()}"

    def clear(self):
        self.attribute_input.clear()
        self.value_input.clear()
