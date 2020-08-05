from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class DirectoryStat(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.text_label = QLabel("", parent=self)
        self.text_label.setStyleSheet('border-style: solid; border-width: 3px; border-color: red;')
        self.layout.addWidget(self.text_label)

    def set_text(self, dir_name, dir_size):
        self.text_label.setText(f"directory name: {dir_name}\n\n\ndirectory size: {dir_size}")