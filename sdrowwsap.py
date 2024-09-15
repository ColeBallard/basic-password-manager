from PyQt5.QtWidgets import QApplication

from pmanager import PManager

if __name__ == '__main__':
    app = QApplication([])
    window = PManager()
    window.show()
    app.exec_()