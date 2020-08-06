from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from FileModel.FileItem import EXTENSHIONS
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice
from PyQt5.QtGui import QPainter, QPen
import functools


class StatisticsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.text_label = QLabel("\n", parent=self)

    def explodeSlice(self, exploded, slice_, v):
        slice_.setExploded(exploded)
        slice_.setLabelVisible(exploded)
        self.text_label.setText(f'num of files: {slice_.value()} \n total size: {v}')

    def load_slices(self):
        series = QPieSeries()
        for i in EXTENSHIONS.keys():
            slice = QPieSlice(i, EXTENSHIONS[i][0])
            v = EXTENSHIONS[i][1]
            slice.setPen(QPen(Qt.black, 2))
            slice.hovered[bool].connect(functools.partial(self.explodeSlice, slice_=slice, v=v))
            series.append(slice)
        return series

    def create_chart(self):
        series = self.load_slices()

        chart = QChart()
        chart.legend().hide()
        chart.addSeries(series)
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTitle("File extensions")

        chartview = QChartView(chart)
        chartview.setRenderHint(QPainter.Antialiasing)
        self.layout.addWidget(chartview)
        self.layout.addWidget(self.text_label)