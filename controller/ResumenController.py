from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QListWidgetItem

from model.CategoriaRepository import CategoriaRepository
from model.TransaccionRepository import TransaccionRepository
from view.PieChartWidget import PieChartWidget
from view.TransaccionWidget import TransaccionWidget


class ResumenController:
    def __init__(self, usuario, ui):
        self.usuario = usuario
        self.ui = ui
        self.repositorio_transacciones = TransaccionRepository()
        self.repositorio_categorias = CategoriaRepository()

    def cargar_datos(self):
        self.inicializar_pie_charts()
        self.cargar_resumen_financiero()
        self.cargar_ultimas_transacciones()
        self.cargar_graficos_categorias()


    def inicializar_pie_charts(self):
        """Inicializa y agrega los widgets de gráficos de pastel a los layouts correspondientes de forma eficiente."""
        # Solo crea los widgets si no existen
        if not hasattr(self, 'pie_ingresos') or self.pie_ingresos is None:
            self.pie_ingresos = PieChartWidget()
        if not hasattr(self, 'pie_egresos') or self.pie_egresos is None:
            self.pie_egresos = PieChartWidget()
        for widget, pie in [
            (self.ui.widgetGraficoIngresos, self.pie_ingresos),
            (self.ui.widgetGraficoEgresos, self.pie_egresos)
        ]:
            layout = widget.layout()
            if layout is None:
                layout = QtWidgets.QVBoxLayout(widget)
                layout.setContentsMargins(0, 0, 0, 0)
            else:
                # Elimina solo los widgets previos, no el layout
                while layout.count():
                    item = layout.takeAt(0)
                    widget_to_remove = item.widget()
                    if widget_to_remove is not None and widget_to_remove is not pie:
                        widget_to_remove.setParent(None)
            # Solo agrega si no está ya en el layout
            if pie.parent() != widget:
                layout.addWidget(pie)

    def cargar_resumen_financiero(self):
        ingresos = self.repositorio_transacciones.cargar_transacciones(self.usuario.username, "ingresos")
        egresos = self.repositorio_transacciones.cargar_transacciones(self.usuario.username, "egresos")
        total_ingresos = sum(i.monto for i in ingresos)
        total_egresos = sum(e.monto for e in egresos)
        saldo = total_ingresos - total_egresos
        self.ui.lblSaldo.setText(f"${saldo:,.2f}")
        self.ui.lblIngresos.setText(f"${total_ingresos:,.2f}")
        self.ui.lblEgresos.setText(f"${total_egresos:,.2f}")

    def cargar_ultimas_transacciones(self):
        ingresos = self.repositorio_transacciones.cargar_transacciones(self.usuario.username, "ingresos")
        egresos = self.repositorio_transacciones.cargar_transacciones(self.usuario.username, "egresos")
        todas = ingresos + egresos
        # Ordenar por fecha descendente (asumiendo formato 'YYYY-MM-DD')
        todas.sort(key=lambda t: t.fecha, reverse=True)
        ultimas = todas[:5]
        self.agregar_transacciones_a_lista(ultimas, self.ui.listTransacciones)

    def agregar_transacciones_a_lista(self, transacciones, list_widget):
        list_widget.clear()
        for transaccion in transacciones:
            item = QListWidgetItem(list_widget)
            widget = TransaccionWidget(transaccion)
            item.setSizeHint(widget.sizeHint())
            list_widget.addItem(item)
            list_widget.setItemWidget(item, widget)
            item.setData(QtCore.Qt.ItemDataRole.UserRole, transaccion)

    def cargar_graficos_categorias(self):
        ingresos = self.repositorio_transacciones.cargar_transacciones(self.usuario.username, "ingresos")
        egresos = self.repositorio_transacciones.cargar_transacciones(self.usuario.username, "egresos")

        # Ingresos por categoría
        categorias_ingresos = self.repositorio_categorias.categorias_ingresos
        labels_ing = [c.nombre for c in categorias_ingresos]
        print(f"Categorías de ingresos: {labels_ing}")
        values_ing = []
        for cat in categorias_ingresos:
            total = sum(i.monto for i in ingresos if i.categoria.id == cat.id)
            values_ing.append(total)
        self.pie_ingresos.set_data(labels_ing, values_ing, title="Ingresos por categoría")
        # Egresos por categoría
        cat_egresos = self.repositorio_categorias.categorias_egresos
        labels_egr = [c.nombre for c in cat_egresos]
        values_egr = []
        for cat in cat_egresos:
            total = sum(e.monto for e in egresos if e.categoria.id == cat.id)
            values_egr.append(total)
        self.pie_egresos.set_data(labels_egr, values_egr, title="Egresos por categoría")
