import unittest
from FileModel.SizeUnit import *


class MyTestCase(unittest.TestCase):
    def test_init(self):
        size = SizeUnit(10000)
        self.assertEqual(size.value, 10000)
        self.assertEqual(size.output_unit, "KB")
        self.assertEqual(size.output_value, 9.77)
        size = SizeUnit()
        self.assertEqual(size.output_unit, "B")

    def test_make_redable(self):
        self.assertEqual(SizeUnit.make_readable(1000), (1000, "B"))
        self.assertEqual(SizeUnit.make_readable(1024), (1, "KB"))
        self.assertEqual(SizeUnit.make_readable(1024), (1.0, "KB"))
        self.assertEqual(SizeUnit.make_readable(10000), (9.77, "KB"))
        self.assertEqual(SizeUnit.make_readable(100000), (97.66, "KB"))
        self.assertEqual(SizeUnit.make_readable(10000000), (9.54, "MB"))
        self.assertEqual(SizeUnit.make_readable(100000000000), (93.13, "GB"))
        self.assertEqual(SizeUnit.make_readable(9999999999999), (9.09, "TB"))

    def test_add(self):
        size = SizeUnit(1000)
        size.add(1000)
        self.assertEqual(size.value, 2000)
        self.assertEqual(size.output_value, 1.95)
        size.add(1000)
        self.assertEqual((size.value, size.output_value, size.output_unit), (3000, 2.93, "KB"))

    def test_str_implementation(self):
        size = SizeUnit(1000)
        self.assertEqual(str(size), "1000.0 B")
        size = SizeUnit(10000)
        self.assertEqual(str(size), "9.77 KB")
        size = SizeUnit(1024)
        self.assertEqual(str(size), "1.0 KB")


if __name__ == '__main__':
    unittest.main()
