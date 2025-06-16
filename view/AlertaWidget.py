from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout
from PyQt6.QtGui import QPixmap, QColor, QFont
from PyQt6.QtCore import Qt

class AlertaWidget(QWidget):
    def __init__(self, tipo_alerta: str, mensaje: str, nivel: str):
        super().__init__()

        # Definimos iconos según tipo de alerta
        iconos = {
            "gasto_presupuesto": "💸",
            "gasto_inusual": "📊",
            "saldo_bajo": "⚠️",
            "ahorro_bajo": "🪙"
        }

        # Definimos color según nivel de severidad
        colores = {
            "alto": "#FF4C4C",     # Rojo fuerte
            "medio": "#FFA500",    # Naranja
            "bajo": "#4CAF50"      # Verde
        }

        self.layout = QHBoxLayout(self)

        # Icono
        self.icono = QLabel(iconos.get(tipo_alerta, "ℹ️"))
        self.icono.setFont(QFont("Arial", 24))
        self.layout.addWidget(self.icono)

        # Texto
        self.texto_layout = QVBoxLayout()
        self.titulo = QLabel(self.obtener_titulo(tipo_alerta))
        self.titulo.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.mensaje = QLabel(mensaje)
        self.mensaje.setWordWrap(True)

        self.texto_layout.addWidget(self.titulo)
        self.texto_layout.addWidget(self.mensaje)
        self.layout.addLayout(self.texto_layout)

        # Estilo general
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {colores.get(nivel, '#E0E0E0')};
                border-radius: 10px;
                padding: 10px;
            }}
            QLabel {{
                color: white;
            }}
        """)

    def obtener_titulo(self, tipo_alerta):
        titulos = {
            "gasto_presupuesto": "Exceso de Gasto",
            "gasto_inusual": "Gasto Inusual",
            "saldo_bajo": "Saldo Bajo",
            "ahorro_bajo": "Ahorro Insuficiente"
        }
        return titulos.get(tipo_alerta, "Alerta")
