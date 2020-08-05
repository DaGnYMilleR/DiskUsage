from PyQt5.QtCore import *

UNITS = ['B', 'KB', 'MB', 'GB', 'TB']


class SortingModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDynamicSortFilter(True)
        self.size_regexp = str()

        self.size_value_is_greater = False
        self.type_regexp = str()
        self.mod_period_is_later = True
        self.mod_regexp = str()
        self.creation_regexp = str()
        self.creation_period_is_later = True

    def lessThan(self, left_index, right_index):
        left_data = self.sourceModel().data(left_index, Qt.DisplayRole)
        right_data = self.sourceModel().data(right_index, Qt.DisplayRole)
        col = left_index.column()
        if col == 0:
            return self.sort_by_name(left_data, right_data)
        if col == 1:
            return self.sort_by_size(left_data, right_data)
        if col == 2:
            return self.sort_by_type(left_data, right_data)
        if col == 3:
            return self.sort_by_time(left_data, right_data)
        if col == 4:
            return self.sort_by_time(left_data, right_data)
        return False

    @staticmethod
    def sort_by_name(first, second):
        return len(first) < len(second)

    @staticmethod
    def sort_by_size(first, second):
        if first is None:
            return True
        if second is None:
            return False
        l_item = first.split()
        r_item = second.split()
        if UNITS.index(l_item[1]) == UNITS.index(r_item[1]):
            return float(l_item[0]) > float(r_item[0])
        return UNITS.index(l_item[1]) > UNITS.index(r_item[1])

    @staticmethod
    def sort_by_type(first, second):
        if first == 'directory':
            return False
        if second == 'directory':
            return True
        return len(first) > len(second)

    @staticmethod
    def sort_by_time(first, second):
        day1, month1, year1 = first.split('.')
        day2, month2, year2 = second.split('.')
        if year1 == year2:
            if month1 == month2:
                return int(day1) > int(day2)
            return int(month1) > int(month2)
        return int(year1) > int(year2)

    def set_size_regexp(self, number=str(), unit=None, param=True):
        self.size_regexp = number if number is str() else f'{number} {unit}'
        self.size_value_is_greater = param == 'greater'

    def set_type_regexp(self, pattern=str()):
        self.type_regexp = pattern

    def set_times_regexp(self, mod_time=str(), mod_period=True, creation_time=None, creation_period=True):
        self.mod_regexp = mod_time
        self.mod_period_is_later = mod_period == 'later'
        self.creation_regexp = creation_time
        self.creation_period_is_later = creation_period == 'later'

    def compare_items(self, regexp, comparable_function, index, condition):
        return True if not regexp else \
            comparable_function(self.sourceModel().data(index, Qt.DisplayRole), regexp) == condition

    def filterAcceptsRow(self, source_row, source_parent):
        size_index = self.sourceModel().index(source_row, 1, source_parent)
        type_index = self.sourceModel().index(source_row, 2, source_parent)
        mod_index = self.sourceModel().index(source_row, 3, source_parent)
        creation_index = self.sourceModel().index(source_row, 4, source_parent)

        compare_by_size = self.compare_items(self.size_regexp, self.sort_by_size, size_index, self.size_value_is_greater)
        compare_by_mod = self.compare_items(self.mod_regexp, self.sort_by_time, mod_index, self.mod_period_is_later)
        compare_by_creation = self.compare_items(self.creation_regexp, self.sort_by_time, creation_index, self.creation_period_is_later)
        compare_by_type = True if not self.type_regexp else self.type_regexp == self.sourceModel().data(type_index, Qt.DisplayRole)

        return all([compare_by_size, compare_by_type, compare_by_mod, compare_by_creation])

