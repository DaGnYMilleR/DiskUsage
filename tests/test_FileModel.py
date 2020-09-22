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


if __name__ == '__main__':
    unittest.main()
