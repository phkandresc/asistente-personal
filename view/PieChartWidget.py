from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCharts import QChart, QChartView, QPieSeries
from PyQt6.QtGui import QPainter
from PyQt6 import QtCore

class PieChartWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.chart = QChart()
        self.chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.layout.addWidget(self.chart_view)
        self.setLayout(self.layout)

    def set_data(self, labels, values, title=""):
        self.chart.removeAllSeries()
        series = QPieSeries()
        total = sum(values)
        if total > 0:
            for label, value in zip(labels, values):
                if value > 0:
                    series.append(f"{label} ({value:.2f})", value)
        else:
            series.append("Sin datos", 1)
        self.chart.addSeries(series)
        self.chart.setTitle(title)
