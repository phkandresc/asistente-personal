from PyQt6.QtWidgets import QCalendarWidget
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import Qt

class CalendarioFinanciero(QCalendarWidget):
    def __init__(self, gastos_por_fecha: dict, parent=None):
        super().__init__(parent)
        self.gastos_por_fecha = gastos_por_fecha  # { 'yyyy-MM-dd' : gasto total del día }
        self.setGridVisible(True)
        self.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)

    def paintCell(self, painter, rect, date):
        super().paintCell(painter, rect, date)

        fecha_str = date.toString("yyyy-MM-dd")
        gasto = self.gastos_por_fecha.get(fecha_str, 0)

        if gasto != 0:
            # Calculamos intensidad (más gasto → más rojo)
            intensidad = min(255, 80 + int(gasto * 0.1))
            color = QColor(220, 0, 0, intensidad)

            painter.save()
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setBrush(color)
            painter.setPen(Qt.PenStyle.NoPen)

            radio = min(rect.width(), rect.height()) // 3
            painter.drawEllipse(rect.center(), radio, radio)

            painter.restore()
