from PyQt5.QtWidgets import QApplication, QListWidget, QListWidgetItem, QMessageBox
from PyQt5.QtCore import Qt

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
            if ':' in text:
                attr, value = text.split(':', 1)  # Split only on the first colon
                self.actual_value = value.strip()
                masked_value = '*' * len(self.actual_value)
                self.setText(f"{attr}: {masked_value}")
            else:
                # Handle the case where there is no colon in the text
                self.setText(text)  # Or any other placeholder you prefer
        else:
            self.setText(text)

    def getActualValue(self):
        return self.actual_value