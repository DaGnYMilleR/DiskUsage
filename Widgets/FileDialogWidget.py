from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class FileDialogWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.Window)
        file_dialog_layout = QVBoxLayout()
        self.setLayout(file_dialog_layout)

        lb = QLabel('Hello! This is disk usage app \n choose working directory')
        lb.setFont(QFont('SansSerif', 20))
        lb.setGeometry(0, 0, 300, 100)

        self.open_file_dialog_button = QPushButton("...Browse...")
        file_dialog_layout.addWidget(lb, alignment=Qt.AlignTop)
        file_dialog_layout.addWidget(self.open_file_dialog_button, 200)

        self.setGeometry(500, 300, 300, 300)
        self.show()