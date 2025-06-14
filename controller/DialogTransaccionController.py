from PyQt6 import QtWidgets, QtCore
from view.DialogTransaccion import Ui_dialogTransaccion
from model.CategoriaRepository import CategoriaRepository
from model.TransaccionRepository import TransaccionRepository
from model.Transaccion import Ingreso, Egreso
from PyQt6.QtCore import QDate, QObject, pyqtSignal

class DialogTransaccionController(QObject):
    transaccion_guardada = pyqtSignal(object)
    transaccion_actualizada = pyqtSignal(object)
    transaccion_eliminada = pyqtSignal(object)

    def __init__(self, usuario, transaccion=None):
        super().__init__()
        self.usuario = usuario
        self.transaccion = transaccion
        # Crear el diálogo y configurar la UI
        self.dialog = QtWidgets.QDialog()
        self.ui = Ui_dialogTransaccion()
        self.ui.setupUi(self.dialog)
        # Inicializar los repositorios
        self.repo_cat = CategoriaRepository()
        self.repo_trans = TransaccionRepository()
        # Configurar el diálogo y conectar señales
        self.configurar_dialogo()
        self.ui.cmbTipoTransaccion.currentTextChanged.connect(self.actualizar_categorias)
        self.ui.btnGuardar.clicked.connect(self.guardar_transaccion)
        self.ui.btnCancelar.clicked.connect(self.dialog.reject)
        self.ui.btnEliminar.clicked.connect(self.eliminar_transaccion)

    def configurar_dialogo(self):
        self.ui.cmbTipoTransaccion.clear()
        self.ui.cmbTipoTransaccion.addItems(["Ingresos",
                                             "Egresos"])
        if self.transaccion:
            tipo = f"{self.transaccion.__class__.__name__}s"
            self.ui.cmbTipoTransaccion.setCurrentText(tipo)
            self.ui.dsbMonto.setValue(self.transaccion.monto)
            self.ui.dateTransaccion.setDate(QDate.fromString(self.transaccion.fecha, "yyyy-MM-dd"))
            self.actualizar_categorias()
            self.ui.cmbCategoria.setCurrentText(self.transaccion.categoria.nombre)
            self.ui.txtDescripcion.setText(self.transaccion.descripcion or "")
            self.ui.btnEliminar.setVisible(True)
        else:
            self.ui.cmbTipoTransaccion.setCurrentText("Ingresos")
            self.ui.dsbMonto.setValue(0.0)
            self.ui.dateTransaccion.setDate(QDate.currentDate())
            self.actualizar_categorias()
            self.ui.txtDescripcion.clear()
            self.ui.btnEliminar.setVisible(False)

    def actualizar_categorias(self, *args):
        tipo = self.ui.cmbTipoTransaccion.currentText()
        if tipo == "Ingresos":
            categorias = self.repo_cat.categorias_ingresos
        else:
            categorias = self.repo_cat.categorias_egresos
        self.ui.cmbCategoria.clear()
        self.ui.cmbCategoria.addItems([c.nombre for c in categorias])

    def guardar_transaccion(self):
        tipo = self.ui.cmbTipoTransaccion.currentText()
        monto = self.ui.dsbMonto.value()
        fecha = self.ui.dateTransaccion.date().toString("yyyy-MM-dd")
        nombre_categoria = self.ui.cmbCategoria.currentText()
        descripcion = self.ui.txtDescripcion.text()
        categorias = self.repo_cat.categorias_ingresos if tipo == "Ingresos" else self.repo_cat.categorias_egresos
        categoria = next((c for c in categorias if c.nombre == nombre_categoria), None)
        if not categoria:
            QtWidgets.QMessageBox.warning(self.dialog, "Error", "Debe seleccionar una categoría válida.")
            return
        if self.transaccion:
            self.transaccion.monto = monto
            self.transaccion.fecha = fecha
            self.transaccion.categoria = categoria
            self.transaccion.descripcion = descripcion
            self.actualizar_transaccion()
            self.transaccion_actualizada.emit(self.transaccion)
        else:
            nuevo_id = self.repo_trans.obtener_nuevo_id(self.usuario.username, tipo)
            if tipo == "Ingresos":
                trans = Ingreso(nuevo_id, monto, fecha, categoria, descripcion)
            else:
                trans = Egreso(nuevo_id, monto, fecha, categoria, descripcion)
            self.repo_trans.registrar_transaccion(self.usuario.username, trans)
            self.transaccion_guardada.emit(trans)
        self.dialog.accept()

    def actualizar_transaccion(self):
        """
        Actualiza la información de la transacción actual (ingreso o egreso) usando repositorio.
        Retorna True si se actualizó correctamente, False si no se encontró la transacción.
        """
        if not self.transaccion:
            return False
        else:
            tipo = self.transaccion.__class__.__name__.lower()
            return self.repo_trans.actualizar_transaccion(self.usuario.username, tipo, self.transaccion)

    def eliminar_transaccion(self):
        if not self.transaccion:
            return
        tipo = self.transaccion.__class__.__name__.lower()
        transacciones = self.repo_trans.cargar_transacciones(self.usuario.username, tipo)
        transacciones = [t for t in transacciones if t.id != self.transaccion.id]
        self.repo_trans.guardar_transacciones(self.usuario.username, tipo, transacciones)
        self.transaccion_eliminada.emit(self.transaccion)
        self.dialog.accept()

    def mostrar(self):
        return self.dialog.exec()
