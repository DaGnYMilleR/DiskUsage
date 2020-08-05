from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class FilterWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.Window)

        information_label = QLabel("      Enter the patterns in the places you need.", self)
        information_label.setFont(QFont('SansSerif', 13))
        information_label.setScaledContents(True)
        information_label.setGeometry(0, 0, 500, 100)
        information_label.setAlignment(Qt.AlignTop)

        type_label = QLabel('filter by type', self)
        type_label.setScaledContents(True)
        type_label.setFont(QFont("Times", 10))
        type_label.setGeometry(5, 45, 300, 20)

        self.type_field = QLineEdit(parent=self)
        self.type_field.setText('.py')
        self.type_field.setGeometry(105, 40, 250, 30)

        mod_label = QLabel('    filter by \n modified date', self)
        mod_label.setScaledContents(True)
        mod_label.setFont(QFont("Times", 10))
        mod_label.setGeometry(5, 86, 200, 50)

        date_regexp = QRegExp("\\d{2}.\\d{2}.\\d{4}")
        date_validator = QRegExpValidator(date_regexp)

        self.mod_field = QLineEdit(parent=self)
        self.mod_field.setText('21.06.2020')
        self.mod_field.setValidator(date_validator)
        self.mod_field.setGeometry(115, 90, 200, 30)

        self.mod_btn_group = QButtonGroup(parent=self)
        self.later_mod_radio = QRadioButton('later', self)
        self.later_mod_radio.setGeometry(350, 80, 100, 30)
        self.earlier_mod_radio = QRadioButton('earlier', self)
        self.earlier_mod_radio.setGeometry(350, 100, 100, 30)
        self.later_mod_radio.setChecked(True)
        self.mod_btn_group.addButton(self.later_mod_radio)
        self.mod_btn_group.addButton(self.earlier_mod_radio)
        self.mod_btn_group.setExclusive(True)

        creation_label = QLabel('    filter by \n creation date', self)
        creation_label.setScaledContents(True)
        creation_label.setFont(QFont("Times", 10))
        creation_label.setGeometry(5, 135, 200, 50)

        self.creation_field = QLineEdit(parent=self)
        self.creation_field.setText('22.06.1488')
        self.creation_field.setValidator(date_validator)
        self.creation_field.setGeometry(115, 140, 200, 30)

        self.creation_btn_group = QButtonGroup(parent=self)
        self.later_creation_radio = QRadioButton('later', self)
        self.later_creation_radio.setGeometry(350, 130, 100, 30)
        self.earlier_creation_radio = QRadioButton('earlier', self)
        self.earlier_creation_radio.setGeometry(350, 150, 100, 30)
        self.later_creation_radio.setChecked(True)
        self.creation_btn_group.addButton(self.later_creation_radio)
        self.creation_btn_group.addButton(self.earlier_creation_radio)
        self.creation_btn_group.setExclusive(True)

        size_label = QLabel('filter by size', self)
        size_label.setScaledContents(True)
        size_label.setFont(QFont("Times", 10))
        size_label.setGeometry(5, 185, 200, 50)

        size_regexp = QRegExp('^[0-9]+$')
        size_validator = QRegExpValidator(size_regexp)
        self.size_field = QLineEdit(parent=self)
        self.size_field.setText('1024')
        self.size_field.setValidator(size_validator)
        self.size_field.setGeometry(115, 190, 100, 30)

        self.units = QComboBox(self)
        self.units.addItems(['B', 'KB', 'MB', 'GB', 'TB'])
        self.units.setGeometry(230, 190, 50, 30)

        self.size_btn_group = QButtonGroup(parent=self)
        self.greater_size_radio = QRadioButton('greater', self)
        self.greater_size_radio.setGeometry(300, 180, 100, 30)
        self.less_size_radio = QRadioButton('less', self)
        self.less_size_radio.setGeometry(300, 200, 100, 30)
        self.greater_size_radio.setChecked(True)
        self.size_btn_group.addButton(self.greater_size_radio)
        self.size_btn_group.addButton(self.less_size_radio)
        self.size_btn_group.setExclusive(True)

        self.apply_button = QPushButton("apply", self)
        self.apply_button.setGeometry(145, 240, 100, 35)

        self.clear_button = QPushButton('clear all', self)
        self.clear_button.setGeometry(260, 240, 100, 35)

        self.set_recursive_filtering_checkbox = QCheckBox('set recursive \n   filtering', self)
        self.set_recursive_filtering_checkbox.move(20, 240)

        self.setGeometry(500, 500, 600, 400)
        self.setFixedSize(500, 300)
        self.setWindowTitle('filter settings')