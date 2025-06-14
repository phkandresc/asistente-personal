from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QListWidgetItem, QMainWindow
from PyQt6.QtCore import QDate

from model.TransaccionRepository import TransaccionRepository
from view.CalendarioFinanciero import CalendarioFinanciero
from controller.DialogTransaccionController import DialogTransaccionController
from view.TransaccionWidget import TransaccionWidget


class TransaccionesController:
    def __init__(self, usuario, ui):
        self.usuario = usuario
        self.ui = ui
        self.repo_trans = TransaccionRepository()
        self.ui.btnAgregarTransaccion.clicked.connect(lambda: self.abrir_dialogo_transaccion())
        self.ui.listTransaccionesPorDia.itemDoubleClicked.connect(lambda item: self.abrir_dialogo_transaccion(item.data(QtCore.Qt.ItemDataRole.UserRole)))
        self.calendario_financiero = None
        self.cargar_datos()

    def configurar_calendario_financiero(self):
        gastos_por_fecha = self.repo_trans.egresos_por_dia(self.usuario.username)
        if self.calendario_financiero is None:
            self.calendario_financiero = CalendarioFinanciero(gastos_por_fecha)

            hoy = QDate.currentDate()
            self.calendario_financiero.setSelectedDate(hoy)
            self.calendario_financiero.showSelectedDate()
            self.calendario_financiero.selectionChanged.connect(self.mostrar_transacciones_del_dia)
        else:
            self.calendario_financiero.set_gastos_por_fecha(gastos_por_fecha) if hasattr(self.calendario_financiero, 'set_gastos_por_fecha') else None
        layout = self.ui.widgetCalendario.layout() or QtWidgets.QVBoxLayout(self.ui.widgetCalendario)
        # Elimina solo widgets previos, no el layout
        while layout.count():
            item = layout.takeAt(0)
            widget_to_remove = item.widget()
            if widget_to_remove is not None and widget_to_remove is not self.calendario_financiero:
                widget_to_remove.deleteLater()
        if self.calendario_financiero.parent() != self.ui.widgetCalendario:
            layout.addWidget(self.calendario_financiero)

    def abrir_dialogo_transaccion(self, transaccion=None):
        dialog_controller = DialogTransaccionController(self.usuario, transaccion)
        dialog_controller.transaccion_actualizada.connect(self.cargar_datos)
        dialog_controller.transaccion_guardada.connect(self.cargar_datos)
        dialog_controller.transaccion_eliminada.connect(self.cargar_datos)
        dialog_controller.mostrar()

    def mostrar_transacciones_del_dia(self):
        qdate = self.calendario_financiero.selectedDate()
        fecha_str = qdate.toString("yyyy-MM-dd")
        ingresos = self.repo_trans.cargar_transacciones_por_dia(self.usuario.username, "ingresos", fecha_str)
        egresos = self.repo_trans.cargar_transacciones_por_dia(self.usuario.username, "egresos", fecha_str)
        transacciones = ingresos + egresos
        transacciones.sort(key=lambda t: t.id, reverse=True)
        self.agregar_transacciones_a_lista(transacciones, self.ui.listTransaccionesPorDia)

    def agregar_transacciones_a_lista(self, transacciones, list_widget):
        list_widget.clear()
        for transaccion in transacciones:
            item = QListWidgetItem(list_widget)
            widget = TransaccionWidget(transaccion)
            item.setSizeHint(widget.sizeHint())
            list_widget.addItem(item)
            list_widget.setItemWidget(item, widget)
            item.setData(QtCore.Qt.ItemDataRole.UserRole, transaccion)

    def cargar_datos(self):
        self.configurar_calendario_financiero()
        self.mostrar_transacciones_del_dia()
        if hasattr(self.ui, 'listTransacciones'):
            self.mostrar_ultimas_transacciones()

    def mostrar_ultimas_transacciones(self):
        ingresos = self.repo_trans.cargar_transacciones(self.usuario.username, "ingresos")
        egresos = self.repo_trans.cargar_transacciones(self.usuario.username, "egresos")
        todas = ingresos + egresos
        todas.sort(key=lambda t: t.fecha, reverse=True)
        ultimas = todas[:5]
        self.agregar_transacciones_a_lista(ultimas, self.ui.listTransacciones)
