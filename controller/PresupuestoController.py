from model.PresupuestoRepository import PresupuestoRepository
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import Qt
from controller.DialogPresupuestoController import DialogPresupuestoController

class PresupuestoController:
    def __init__(self, usuario, ui):
        self.usuario = usuario
        self.ui = ui
        self.repo = PresupuestoRepository()
        self.ui.datePresupuesto.dateChanged.connect(self.llenar_tabla_presupuesto)
        self.ui.datePresupuesto.setDate(QtCore.QDate.currentDate())
        self.ui.tablaPresupuestoMensual.setColumnCount(4)
        self.ui.tablaPresupuestoMensual.setHorizontalHeaderLabels(["Categoría", "Guardado", "% Cumplimiento", "Objetivo"])
        self.conectar_dialogo_presupuesto()

    def cargar_datos(self):
        """Carga los datos iniciales del presupuesto."""
        self.ajustar_tabla_presupuesto()
        self.llenar_tabla_presupuesto()

    def ajustar_tabla_presupuesto(self):
        """Ajusta el tamaño de las columnas y filas de la tabla para que el contenido se vea bien visualmente."""
        tabla = self.ui.tablaPresupuestoMensual
        tabla.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        tabla.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        tabla.setWordWrap(True)
        tabla.setAlternatingRowColors(True)

    def llenar_tabla_presupuesto(self):
        """Llena la tabla con los datos del presupuesto del mes/año seleccionados."""
        # Obtener mes y año desde el widget de fecha
        qdate = self.ui.datePresupuesto.date()
        mes = str(qdate.month()).zfill(2)
        anio = str(qdate.year())
        try:
            presupuesto_mensual = self.repo.cargar_presupuesto_mensual(self.usuario.username, mes, anio)
        except Exception:
            # Si no hay presupuesto, limpiar la tabla
            self.ui.tablaPresupuestoMensual.setRowCount(0)
            self.ajustar_tabla_presupuesto()
            return
        self.ui.tablaPresupuestoMensual.setRowCount(len(presupuesto_mensual.presupuestos))
        self.ui.tablaPresupuestoMensual.setColumnCount(4)
        self.ui.tablaPresupuestoMensual.setHorizontalHeaderLabels([
            "Categoría", "Guardado", "% Cumplimiento", "Objetivo"
        ])
        for fila, presupuesto in enumerate(presupuesto_mensual.presupuestos):
            # Columna 0: Categoría (solo lectura)
            item_categoria = QtWidgets.QTableWidgetItem(presupuesto.categoria.nombre)
            item_categoria.setFlags(Qt.ItemFlag.ItemIsEnabled)
            self.ui.tablaPresupuestoMensual.setItem(fila, 0, item_categoria)
            # Columna 1: Guardado (solo lectura)
            item_guardado = QtWidgets.QTableWidgetItem(f"{presupuesto.monto_guardado:.2f}")
            item_guardado.setFlags(Qt.ItemFlag.ItemIsEnabled)
            self.ui.tablaPresupuestoMensual.setItem(fila, 1, item_guardado)
            # Columna 2: ProgressBar de % Cumplimiento
            porcentaje = int((presupuesto.monto_guardado / presupuesto.monto_objetivo) * 100) if presupuesto.monto_objetivo else 0
            progress = QtWidgets.QProgressBar()
            progress.setValue(porcentaje)
            progress.setFormat(f"{porcentaje}%")
            progress.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.ui.tablaPresupuestoMensual.setCellWidget(fila, 2, progress)
            # Columna 3: Monto Objetivo (editable)
            item_objetivo = QtWidgets.QTableWidgetItem(f"{presupuesto.monto_objetivo:.2f}")
            item_objetivo.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsEnabled)
            self.ui.tablaPresupuestoMensual.setItem(fila, 3, item_objetivo)
        self.ajustar_tabla_presupuesto()

    def conectar_dialogo_presupuesto(self):
        self.ui.btnNuevoPresupuesto.clicked.connect(self.abrir_dialogo_presupuesto)
        self.ui.tablaPresupuestoMensual.cellDoubleClicked.connect(self.abrir_edicion_presupuesto)

    def abrir_dialogo_presupuesto(self):
        qdate = self.ui.datePresupuesto.date()
        mes = str(qdate.month()).zfill(2)
        anio = str(qdate.year())
        dialog_ctrl = DialogPresupuestoController(self.usuario, mes=mes, anio=anio)
        dialog_ctrl.presupuesto_guardado.connect(lambda p: self.llenar_tabla_presupuesto())
        dialog_ctrl.presupuesto_actualizado.connect(lambda p: self.llenar_tabla_presupuesto())
        dialog_ctrl.presupuesto_eliminado.connect(lambda p: self.llenar_tabla_presupuesto())
        dialog_ctrl.dialog.exec()

    def abrir_edicion_presupuesto(self, row, column):
        qdate = self.ui.datePresupuesto.date()
        mes = str(qdate.month()).zfill(2)
        anio = str(qdate.year())
        self.presupuesto_seleccionado = None
        try:
            presupuesto_mensual = self.repo.cargar_presupuesto_mensual(self.usuario.username, mes, anio)
            # Obtener el nombre de la categoría de la fila seleccionada
            nombre_categoria = self.ui.tablaPresupuestoMensual.item(row, 0).text()
            # Buscar el presupuesto por nombre de categoría
            self.presupuesto_seleccionado = next((p for p in presupuesto_mensual.presupuestos if p.categoria.nombre == nombre_categoria), None)
        except Exception:
            return
        if not self.presupuesto_seleccionado:
            return
        dialog_ctrl = DialogPresupuestoController(self.usuario, presupuesto=self.presupuesto_seleccionado, mes=mes, anio=anio)
        dialog_ctrl.presupuesto_guardado.connect(lambda p: self.llenar_tabla_presupuesto())
        dialog_ctrl.presupuesto_actualizado.connect(lambda p: self.llenar_tabla_presupuesto())
        dialog_ctrl.presupuesto_eliminado.connect(lambda p: self.llenar_tabla_presupuesto())
        dialog_ctrl.dialog.exec()
