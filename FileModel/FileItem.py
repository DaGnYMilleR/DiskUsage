import os
import sys
import datetime
import time
import math
from FileModel.SizeUnit import SizeUnit
from collections import defaultdict

EXTENSHIONS = dict()


class FileItem:
    def __init__(self, path=None, parent=None):
        """
        This class contains all information about file and it's implementation
        itemData = [name, size, type(directory if folder), modified date, creation date]
        :param path: path to the file or folder
        :param parent: parent of this file or folder
        """
        self.parentItem = parent
        self.childItems = list()
        self.full_path = path
        self.itemData = self.get_file_info(path) if path is not None else [None, None, None, None, None]


    def get_file_info(self, path):
        name = os.path.basename(path)
        item_name = os.path.splitext(name)
        try:
            size = os.path.getsize(path)
            if os.path.isdir(path):
                item_type = 'directory'
                size = 0
            else:
                item_type = item_name[-1]
                if item_type:
                    if EXTENSHIONS.get(item_type):
                        EXTENSHIONS[item_type][0] += 1
                        EXTENSHIONS[item_type][1].add(size)
                    else:
                        EXTENSHIONS[item_type] = [0, SizeUnit()]
                if self.parentItem is None:
                    return
                self.increase_size_to_all_parents(size, self.parentItem)
            return [item_name[0], SizeUnit(size), item_type, self.time_handler(os.path.getmtime(path)), self.time_handler(os.path.getctime(path))]
        except OSError:
            return [item_name[0], None, None, None, None]

    @staticmethod
    def time_handler(time_str):
        try:
            return datetime.datetime.fromtimestamp(time_str).strftime("%d.%m.%Y")
        except TypeError:
            return "03.10.2001"

    def increase_size_to_all_parents(self, value, parent):
        while parent is not None and parent.full_path is not None and parent.itemData[1] is not None:
            parent.itemData[1].add(value)
            parent = parent.parent()

    def appendChild(self, item):
        self.childItems.append(item)

    def child(self, row):
        try:
            return self.childItems[row]
        except IndexError:
            return None

    def childCount(self):
        return len(self.childItems)

    def columnCount(self):
        return len(self.itemData)

    def data(self, column):
        try:
            if column == 1:
                return str(self.itemData[1])
            return self.itemData[column]
        except IndexError:
            return None

    def parent(self):
        return self.parentItem

    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)
        return 0

