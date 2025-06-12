from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QPushButton, QMainWindow, QListWidgetItem

from view.TransaccionWidget import TransaccionWidget
from view.ventanaPrincipal import Ui_ventanaPrincipal
from model.TransaccionRepository import TransaccionRepository
from view.PieChartWidget import PieChartWidget
from model.CategoriaRepository import CategoriaRepository


class MainController:
    def __init__(self, usuario):
        self.vista = QMainWindow()

        self.ui = Ui_ventanaPrincipal()
        self.ui.setupUi(self.vista)

        self.ui.widgetMenuIconos.hide()
        self.ui.pilaWidgets.setCurrentIndex(0)
        self.ui.btnResumen.setChecked(True)

        self.ui.btnResumen.toggled.connect(lambda: self.cambiar_pagina(0))

        # Usuario con credenciales correctas
        self.usuario = usuario
        self.ui.lblUsername.setText(f"Bienvenido, {self.usuario.nombre} {self.usuario.apellido}")

        # Widgets de gráficos de pastel
        self.pie_ingresos = PieChartWidget()
        self.pie_egresos = PieChartWidget()
        # Limpiar y agregar los widgets de pastel a los contenedores
        layout_ingresos = QtWidgets.QVBoxLayout(self.ui.widgetGraficoIngresos)
        layout_ingresos.setContentsMargins(0, 0, 0, 0)
        layout_ingresos.addWidget(self.pie_ingresos)
        layout_egresos = QtWidgets.QVBoxLayout(self.ui.widgetGraficoEgresos)
        layout_egresos.setContentsMargins(0, 0, 0, 0)
        layout_egresos.addWidget(self.pie_egresos)

        # Cargar datos financieros
        self.cargar_resumen_financiero()
        self.cargar_ultimas_transacciones()
        self.cargar_graficos_categorias()

    def cargar_resumen_financiero(self):
        repo = TransaccionRepository()
        ingresos = repo.cargar_transacciones(self.usuario.username, "ingresos")
        egresos = repo.cargar_transacciones(self.usuario.username, "egresos")
        total_ingresos = sum(i.monto for i in ingresos)
        total_egresos = sum(e.monto for e in egresos)
        saldo = total_ingresos - total_egresos
        self.ui.lblSaldo.setText(f"${saldo:,.2f}")
        self.ui.lblIngresos.setText(f"${total_ingresos:,.2f}")
        self.ui.lblEgresos.setText(f"${total_egresos:,.2f}")


    # Dar color si es ingreso o egreso
    def cargar_ingresos(self):
        repo = TransaccionRepository()
        ingresos = repo.cargar_transacciones(self.usuario.username, "ingresos")
        print(f"Transacciones cargadas: {len(ingresos)}")
        self.ui.listTransacciones.clear()

        for ingreso in ingresos:
            item = QListWidgetItem(self.ui.listTransacciones)
            widget = TransaccionWidget(ingreso)
            item.setSizeHint(widget.sizeHint())
            self.ui.listTransacciones.addItem(item)
            self.ui.listTransacciones.setItemWidget(item, widget)

    def cargar_ultimas_transacciones(self):
        repo = TransaccionRepository()
        ingresos = repo.cargar_transacciones(self.usuario.username, "ingresos")
        egresos = repo.cargar_transacciones(self.usuario.username, "egresos")
        todas = ingresos + egresos
        # Ordenar por fecha descendente (asumiendo formato 'YYYY-MM-DD')
        todas.sort(key=lambda t: t.fecha, reverse=True)
        ultimas = todas[:5]
        self.ui.listTransacciones.clear()
        for transaccion in ultimas:
            item = QListWidgetItem(self.ui.listTransacciones)
            widget = TransaccionWidget(transaccion)
            item.setSizeHint(widget.sizeHint())
            self.ui.listTransacciones.addItem(item)
            self.ui.listTransacciones.setItemWidget(item, widget)

    def cargar_graficos_categorias(self):
        repo = TransaccionRepository()
        categorias_repo = CategoriaRepository()
        ingresos = repo.cargar_transacciones(self.usuario.username, "ingresos")
        egresos = repo.cargar_transacciones(self.usuario.username, "egresos")

        # Ingresos por categoría
        categorias_ingresos = categorias_repo.categorias_ingresos
        labels_ing = [c.nombre for c in categorias_ingresos]
        print(f"Categorías de ingresos: {labels_ing}")
        values_ing = []
        for cat in categorias_ingresos:
            total = sum(i.monto for i in ingresos if i.categoria.id == cat.id)
            values_ing.append(total)
        self.pie_ingresos.set_data(labels_ing, values_ing, title="Ingresos por categoría")
        # Egresos por categoría
        cat_egresos = categorias_repo.categorias_egresos
        labels_egr = [c.nombre for c in cat_egresos]
        values_egr = []
        for cat in cat_egresos:
            total = sum(e.monto for e in egresos if e.categoria.id == cat.id)
            values_egr.append(total)
        self.pie_egresos.set_data(labels_egr, values_egr, title="Egresos por categoría")

    def cambiar_pagina(self, index: int):
        self.ui.pilaWidgets.setCurrentIndex(index)

    ## Change QPushButton Checkable status when stackedWidget index changed
    def on_stackedWidget_currentChanged(self, index):
        btn_list = self.ui.widgetMenuIconos.findChildren(QPushButton) \
                   + self.ui.widgetMenu.findChildren(QPushButton)

        for btn in btn_list:
            if index in [5, 6]:
                btn.setAutoExclusive(False)
                btn.setChecked(False)
            else:
                btn.setAutoExclusive(True)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    controlador = MainController()
    controlador.vista.show()
    sys.exit(app.exec())
