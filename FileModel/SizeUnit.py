UNITS = ['B', 'KB', 'MB', 'GB', 'TB']


class SizeUnit:
    def __init__(self, size=0):
        self.value = float(size)
        self.output_value, self.output_unit = self.make_readable(self.value)

    def add(self, other_size):
        self.value += other_size
        self.output_value, self.output_unit = self.make_readable(self.value)

    @staticmethod
    def make_readable(size):
        divider = 1024

        for unit in UNITS:
            if size < divider:
                return round(size, 2), unit
            size /= divider

    def __str__(self):
        return f"{self.output_value} {self.output_unit}"

