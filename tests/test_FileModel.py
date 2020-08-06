import unittest
from FileModel.FileModel import *
import os


class MyTestCase(unittest.TestCase):
    def test_init(self):
        current_dir = os.getcwd()
        model = FileModel(current_dir)
        self.assertEqual(model.path, current_dir)
        model.setup_model_data(model.root, model.path)
        self.assertEqual(type(model.root), type(model.rootItem))

    def test_header_data(self):
        model = FileModel("current_dir")
        self.assertEqual(model.headerData(0, Qt.Horizontal, 0), "Name")
        self.assertEqual(model.headerData(1, Qt.Horizontal, 0), "size")
        self.assertEqual(model.headerData(2, Qt.Horizontal, 0), "type")
        self.assertEqual(model.headerData(3, Qt.Horizontal, 0), "modified date")
        self.assertEqual(model.headerData(4, Qt.Horizontal, 0), "creation date")
        self.assertEqual(model.headerData(10, Qt.Horizontal, 0), None)


if __name__ == '__main__':
    unittest.main()
