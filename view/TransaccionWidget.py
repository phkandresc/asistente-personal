from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class TransaccionWidget(QWidget):
    def __init__(self, transaccion):
        super().__init__()

        descripcion = transaccion.descripcion
        categoria = transaccion.categoria.nombre
        fecha = transaccion.fecha
        monto = transaccion.monto

        # Layout principal horizontal
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(20)

        # Columna izquierda (descripción, categoría)
        vbox_izq = QVBoxLayout()

        lbl_descripcion = QLabel(descripcion)
        lbl_descripcion.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        vbox_izq.addWidget(lbl_descripcion)

        lbl_categoria = QLabel(categoria)
        lbl_categoria.setStyleSheet("color: #7f8c8d; font-size: 10pt;")
        vbox_izq.addWidget(lbl_categoria)

        layout.addLayout(vbox_izq)

        # Spacer para empujar monto y fecha a la derecha
        layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        # Columna derecha (fecha, monto)
        vbox_der = QVBoxLayout()

        lbl_fecha = QLabel(fecha)
        lbl_fecha.setStyleSheet("color: #95a5a6; font-size: 9pt;")
        lbl_fecha.setAlignment(Qt.AlignmentFlag.AlignRight)
        vbox_der.addWidget(lbl_fecha)

        lbl_monto = QLabel(f"${monto:,.2f}")
        color_monto = "green" if monto >= 0 else "red"
        lbl_monto.setStyleSheet(f"color: {color_monto}; font-weight: bold; font-size: 12pt;")
        lbl_monto.setAlignment(Qt.AlignmentFlag.AlignRight)
        vbox_der.addWidget(lbl_monto)

        layout.addLayout(vbox_der)

        self.setLayout(layout)
        self.setStyleSheet("background-color: #f8f9fa; border: 1px solid #dcdcdc; border-radius: 8px;")
