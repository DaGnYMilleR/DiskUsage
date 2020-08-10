from PyQt5.QtCore import QAbstractItemModel
from PyQt5.QtCore import QModelIndex
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from FileModel.FileItem import FileItem
import os
import threading
import multiprocessing


class FileModel(QAbstractItemModel):
    def __init__(self, path, parent=None):
        super(FileModel, self).__init__(parent)
        self.rootItem = FileItem()
        self.root = FileItem(path, self.rootItem)
        self.path = path
        self.rootItem.appendChild(self.root)

    def setup_model(self):
        self.file_icon = QIcon(os.path.join('images', 'file_gray.jpg'))
        self.folder_icon = QIcon(os.path.join('images', 'folder_image.png'))
        self.setup_model_data(self.root, self.path)

    def columnCount(self, parent=None):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        return self.rootItem.columnCount()

    def data(self, index, role=None):
        if not index.isValid():
            return None
        if role == Qt.DisplayRole:
            item = index.internalPointer()
            return item.data(index.column())

        if role == Qt.DecorationRole:
            if index.column() == 0:
                item = index.internalPointer()
                item_data = item.data(2)
                if item_data == 'directory':
                    return self.folder_icon
                return self.file_icon

        return None

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def headerData(self, section, orientation, role=0):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if section == 0:
                return 'Name'
            elif section == 1:
                return 'size'
            elif section == 2:
                return 'type'
            elif section == 3:
                return 'modified date'
            elif section == 4:
                return 'creation date'
        return None

    def index(self, row, column, parent=None):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()
        if not parent.isValid():
            parent_item = self.rootItem
        else:
            parent_item = parent.internalPointer()

        child_item = parent_item.child(row)
        if child_item:
            return self.createIndex(row, column, child_item)
        return QModelIndex()

    def parent(self, child):
        if not child.isValid():
            return QModelIndex()
        child_item = child.internalPointer()
        parent_item = child_item.parent()
        if parent_item == self.rootItem:
            return QModelIndex()
        return self.createIndex(parent_item.row(), 0, parent_item)

    def rowCount(self, parent=None):
        if parent.column() > 0:
            return 0
        if not parent.isValid():
            parent_item = self.rootItem
        else:
            parent_item = parent.internalPointer()
        return parent_item.childCount()

    def setup_model_data(self, parent, path):
        """
        build FileModel
        :param parent: rootItem
        :param path: path to file
        :return:
        """
        threads = []
        for item in os.listdir(path):
            current_path = os.path.join(path, item)
            if os.path.isfile(current_path):
                parent.appendChild(FileItem(current_path, parent))
            elif os.path.isdir(current_path):
                child = FileItem(current_path, parent)
                tr = threading.Thread(target=self.add_children, args=(child, current_path))
                threads.append(tr)
                tr.start()
                parent.appendChild(child)

        for tr in threads:
            tr.join()

    @staticmethod
    def add_children(parent, path):
        """
        scan directory
        :param parent:
        :param path:
        :return:
        """
        parents = [parent]
        for current_dir, dirs, files in os.walk(path):
            current = parents.pop()
            for dir in dirs[::-1]:
                path_to_dir = os.path.join(current_dir, dir)
                child = FileItem(path_to_dir, current)
                current.appendChild(child)
                parents.append(child)
            for file in files:
                path_to_file = os.path.join(current_dir, file)
                child = FileItem(path_to_file, current)
                current.appendChild(child)