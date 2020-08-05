import unittest
from FileModel.FileItem import *
import datetime

#coverage run -m unittest discover -s "tests" -v


class MyTestCase(unittest.TestCase):
    def test_time_handler(self):
        self.assertEqual(FileItem.time_handler(14882281337), "07.08.2441")
        self.assertEqual(FileItem.time_handler("14882281337"), "03.10.2001")
        self.assertEqual(FileItem.time_handler(True), "01.01.1970")

    def test_init(self):
        item = FileItem()
        self.assertEqual((item.full_path, item.parentItem), (None, None))
        self.assertEqual(item.columnCount(), 5)
        self.assertEqual(item.row(), 0)
        self.assertEqual(item.parent(), None)
        self.assertEqual(item.childCount(), 0)
        item.appendChild("test")
        self.assertEqual(item.childCount(), 1)
        self.assertEqual(item.child(0), "test")
        self.assertEqual(item.child(3), None)
        self.assertEqual(item.data(0), None)
        self.assertEqual(item.data(1), 'None')
        self.assertEqual(item.data(10), None)



if __name__ == '__main__':
    unittest.main()
