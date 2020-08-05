from PyQt5.QtWidgets import *
from PyQt5 import QtCore
import threading
from FileModel.FileModel import FileModel
from FileModel.SortingModel import SortingModel
from Widgets.FilterWidget import FilterWidget
from Widgets.FileDialogWidget import FileDialogWidget
import time
from Widgets.StatisticsWidget import StatisticsWidget


def thread(func):
    def wrapper(*args, **kwargs):
        my_thread = threading.Thread(target=func, args=args, kwargs=kwargs, daemon=True)
        my_thread.start()
    return wrapper


class MainWindow(QMainWindow):
    setup_model_signal = QtCore.pyqtSignal()
    progress_bar_signal = QtCore.pyqtSignal(float)

    def __init__(self):
        super().__init__()

        self.file_dialog_widget = FileDialogWidget(self)

        self.file_dialog_widget.open_file_dialog_button.clicked.connect(self.choose_start_folder)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setMaximum(100)

        self.stat_widget = StatisticsWidget()

        self.model = None

        self.filter_widget = FilterWidget(self)
        self.showMaximized()
        self.setWindowTitle("Disk Usage")
        self.show()

    def on_count_changed(self, value):
        self.progress_bar.setValue(value)

    def set_model(self, path):
        self.model = FileModel(path)

    @thread
    def load_model_data(self, signal, path):
        """
        load information about directory and create model
        :param signal: QtCore.pyqtSignal
        :param path: string
        :return:
        """
        self.model = FileModel(path)
        signal.emit()

    @thread
    def progress_bar_value_handler(self, signal):
        value = 0
        while value < 100:

            if self.model is None:
                signal.emit(value)
                if value == 99:
                    time.sleep(1)
                    continue
            else:
                value = 100
                signal.emit(value)
            time.sleep(1)
            value += 1

    def set_window_after_choosing_directory(self):
        """
        state 2: directory chosen
        creates buttons and grid
        :return:
        """
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.proxy = SortingModel()
        self.treeView = QTreeView()

        self.treeView.setSortingEnabled(True)

        self.grid = QGridLayout()
        self.central_widget.setLayout(self.grid)

        filter_button = QPushButton("filter settings")
        filter_button.clicked.connect(self.open_filter_widget)

        reset_button = QPushButton("reset filter settings")
        reset_button.clicked.connect(self.reset_filter_settings)

        self.grid.setSpacing(10)
        self.grid.addWidget(self.treeView, 0, 0, 5, 7)
        self.grid.addWidget(self.stat_widget, 0, 7, 5, 5)
        self.grid.addWidget(filter_button, 6, 1, 1, 2)
        self.grid.addWidget(reset_button, 6, 3, 1, 2)
        self.grid.addWidget(self.progress_bar, 7, 0, 1, 12)



    def reset_filter_settings(self):
        """
        reset button callback
        :return:
        """
        self.proxy.set_size_regexp()
        self.proxy.set_type_regexp()
        self.proxy.set_times_regexp()
        self.proxy.invalidateFilter()

    def open_filter_widget(self):
        """
        filter button callback
        :return:
        """
        if self.filter_widget.isHidden():
            self.filter_widget.show()
        else:
            self.filter_widget.hide()

        def set_regexp_to_proxy():
            self.proxy.set_size_regexp(self.filter_widget.size_field.text(), self.filter_widget.units.currentText(),
                                       self.filter_widget.size_btn_group.checkedButton().text())
            self.proxy.set_type_regexp(self.filter_widget.type_field.text())
            self.proxy.set_times_regexp(self.filter_widget.mod_field.text(), self.filter_widget.mod_btn_group.checkedButton().text(),
                                        self.filter_widget.creation_field.text(), self.filter_widget.creation_btn_group.checkedButton().text())
            self.proxy.invalidateFilter()

        def update_filter():
            self.filter_widget.size_field.setText(str())
            self.filter_widget.type_field.setText(str())
            self.filter_widget.mod_field.setText(str())
            self.filter_widget.creation_field.setText(str())

        self.filter_widget.apply_button.clicked.connect(set_regexp_to_proxy)
        self.filter_widget.clear_button.clicked.connect(update_filter)
        self.filter_widget.set_recursive_filtering_checkbox.stateChanged.connect(
            lambda: self.proxy.setRecursiveFilteringEnabled(not self.proxy.isRecursiveFilteringEnabled()))

    def model_signal_handler(self):
        """
        file model downloaded
        :return:
        """
        self.proxy.setSourceModel(self.model)
        self.treeView.setModel(self.proxy)
        self.treeView.setColumnWidth(0, 300)
        self.stat_widget.create_chart()

    def set_progress_bar_value(self, value):
        self.progress_bar.setValue(int(value))

    def choose_start_folder(self):
        dir_list = QFileDialog.getExistingDirectory(self.file_dialog_widget, "Choose")
        self.file_dialog_widget.hide()
        self.load_model_data(self.setup_model_signal, dir_list)
        self.setup_model_signal.connect(self.model_signal_handler)

        self.progress_bar_value_handler(self.progress_bar_signal)
        self.progress_bar_signal.connect(self.set_progress_bar_value)

        self.set_window_after_choosing_directory()


if __name__ == '__main__':
    app = QApplication([])
    win = MainWindow()
    app.exec_()