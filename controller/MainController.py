from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QPushButton, QMainWindow, QListWidgetItem

from model.UserRepository import UserRepository
from view.CalendarioFinanciero import CalendarioFinanciero
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
        self.ui.btnTransacciones.toggled.connect(lambda: self.cambiar_pagina(1))
        self.usuario = usuario
        self.ui.lblUsername.setText(f"Bienvenido, {self.usuario.nombre} {self.usuario.apellido}")
        self.inicializar_pie_charts()
        self.cargar_resumen_financiero()
        self.cargar_ultimas_transacciones()
        self.cargar_graficos_categorias()
        self.configurar_calendario_financiero()  # Asegura que el calendario se configure al iniciar

    def inicializar_pie_charts(self):
        """Inicializa y agrega los widgets de gráficos de pastel a los layouts correspondientes."""
        self.pie_ingresos = PieChartWidget()
        self.pie_egresos = PieChartWidget()
        for widget, pie in [
            (self.ui.widgetGraficoIngresos, self.pie_ingresos),
            (self.ui.widgetGraficoEgresos, self.pie_egresos)
        ]:
            layout = QtWidgets.QVBoxLayout(widget)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.addWidget(pie)

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
        self.agregar_transacciones_a_lista(ingresos, self.ui.listTransacciones)

    def agregar_transacciones_a_lista(self, transacciones, list_widget):
        list_widget.clear()
        for transaccion in transacciones:
            item = QListWidgetItem(list_widget)
            widget = TransaccionWidget(transaccion)
            item.setSizeHint(widget.sizeHint())
            list_widget.addItem(item)
            list_widget.setItemWidget(item, widget)

    def cargar_ultimas_transacciones(self):
        repo = TransaccionRepository()
        ingresos = repo.cargar_transacciones(self.usuario.username, "ingresos")
        egresos = repo.cargar_transacciones(self.usuario.username, "egresos")
        todas = ingresos + egresos
        # Ordenar por fecha descendente (asumiendo formato 'YYYY-MM-DD')
        todas.sort(key=lambda t: t.fecha, reverse=True)
        ultimas = todas[:5]
        self.agregar_transacciones_a_lista(ultimas, self.ui.listTransacciones)

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

    def configurar_calendario_financiero(self):
        repo = TransaccionRepository()

        gastos_por_fecha = repo.egresos_por_dia(self.usuario.username)

        self.calendario_financiero = CalendarioFinanciero(gastos_por_fecha)
        self.calendario_financiero.selectionChanged.connect(self.mostrar_transacciones_del_dia)

        # Limpiar el layout donde va el calendario
        layout = self.ui.widgetCalendario.layout() or QtWidgets.QVBoxLayout(self.ui.widgetCalendario)
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        layout.addWidget(self.calendario_financiero)

    def mostrar_transacciones_del_dia(self):
        from model.TransaccionRepository import TransaccionRepository
        repo = TransaccionRepository()

        qdate = self.calendario_financiero.selectedDate()
        fecha_str = qdate.toString("yyyy-MM-dd")

        ingresos = repo.cargar_transacciones_por_dia(self.usuario.username, "ingresos", fecha_str)
        egresos = repo.cargar_transacciones_por_dia(self.usuario.username, "egresos", fecha_str)
        transacciones = ingresos + egresos
        transacciones.sort(key=lambda t: t.id, reverse=True)

        self.agregar_transacciones_a_lista(transacciones, self.ui.listTransaccionesPorDia)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    repositorio = UserRepository()
    print(repositorio.usuarios)
    usuario_prueba = repositorio.validar_credenciales("phkandres", "phkandres")
    controlador = MainController(usuario_prueba)
    controlador.vista.show()
    sys.exit(app.exec())
