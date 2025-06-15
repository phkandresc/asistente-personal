from PyQt6 import QtWidgets
from PyQt6.QtCore import QObject, pyqtSignal

from model.CategoriaRepository import CategoriaRepository
from model.Presupuesto import Presupuesto
from model.PresupuestoRepository import PresupuestoRepository
from view.dialogPresupuesto import Ui_dialogPresupuesto


class DialogPresupuestoController(QObject):
    presupuesto_guardado = pyqtSignal(object)
    presupuesto_actualizado = pyqtSignal(object)
    presupuesto_eliminado = pyqtSignal(object)

    def __init__(self, usuario, presupuesto=None, mes=None, anio=None):
        super().__init__()
        self.usuario = usuario
        self.presupuesto = presupuesto
        self.mes = mes
        self.anio = anio
        print("INFO CARGADA DESDE PRESUPUESTO CONTROLLER")
        print(mes, anio)
        # Crear el diálogo y configurar la UI
        self.dialog = QtWidgets.QDialog()
        self.ui = Ui_dialogPresupuesto()
        self.ui.setupUi(self.dialog)
        # Inicializar los repositorios
        self.repo_categorias = CategoriaRepository()
        self.repo_presupuesto = PresupuestoRepository()
        # Configurar el diálogo y conectar señales
        self.configurar_dialogo()
        self.ui.btnGuardar.clicked.connect(self.guardar_presupuesto)
        self.ui.btnCancelar.clicked.connect(self.dialog.reject)
        self.ui.btnEliminar.clicked.connect(self.eliminar_presupuesto)

    def configurar_dialogo(self):
        self.cargar_categorias()
        if self.presupuesto:
            self.ui.cmbCategoria.setCurrentText(self.presupuesto.categoria.nombre)
            self.ui.dsbMontoObjetivo.setValue(self.presupuesto.monto_objetivo)
            self.ui.btnEliminar.setVisible(True)
        else:
            self.ui.dsbMontoObjetivo.setValue(0.0)
            self.ui.btnEliminar.setVisible(False)

    def cargar_categorias(self):
        categorias = self.repo_categorias.categorias_egresos
        self.ui.cmbCategoria.clear()
        self.ui.cmbCategoria.addItems([c.nombre for c in categorias])

    def guardar_presupuesto(self):
        categoria_nombre = self.ui.cmbCategoria.currentText()
        monto_objetivo = self.ui.dsbMontoObjetivo.value()
        categorias = self.repo_categorias.categorias_egresos
        categoria = next((c for c in categorias if c.nombre == categoria_nombre), None)
        if not categoria:
            QtWidgets.QMessageBox.warning(self.dialog, "Error", "Debe seleccionar una categoría válida.")
            return
        if monto_objetivo <= 0:
            QtWidgets.QMessageBox.warning(self.dialog, "Error", "El monto objetivo debe ser mayor a cero.")
            return
        # Crear o actualizar presupuesto
        from model.Presupuesto import Presupuesto
        presupuesto = self.presupuesto or Presupuesto(categoria=categoria, monto_guardado=0.00, monto_objetivo=monto_objetivo)
        presupuesto.categoria = categoria
        presupuesto.monto_objetivo = monto_objetivo
        # Guardar presupuesto mensual
        mensual = None
        try:
            mensual = self.repo_presupuesto.cargar_presupuesto_mensual(self.usuario.username, self.mes, self.anio)
        except Exception:
            from model.Presupuesto import PresupuestoMensual
            mensual = PresupuestoMensual(presupuestos=[])
        # Verificar si ya existe presupuesto para la categoría
        idx = next((i for i, p in enumerate(mensual.presupuestos) if p.categoria.id == categoria.id), None)
        if idx is not None:
            mensual.presupuestos[idx] = presupuesto
            self.repo_presupuesto.guardar_presupuesto_mensual(self.usuario.username, self.mes, self.anio, mensual)
            self.presupuesto_actualizado.emit(presupuesto)
        else:
            mensual.presupuestos.append(presupuesto)
            self.repo_presupuesto.guardar_presupuesto_mensual(self.usuario.username, self.mes, self.anio, mensual)
            self.presupuesto_guardado.emit(presupuesto)
        self.dialog.accept()

    def eliminar_presupuesto(self):
        if not self.presupuesto:
            return
        try:
            mensual = self.repo_presupuesto.cargar_presupuesto_mensual(self.usuario.username, self.mes, self.anio)
        except Exception:
            return
        mensual.presupuestos = [p for p in mensual.presupuestos if p.categoria.id != self.presupuesto.categoria.id]
        self.repo_presupuesto.guardar_presupuesto_mensual(self.usuario.username, self.mes, self.anio, mensual)
        self.presupuesto_eliminado.emit(self.presupuesto)
        self.dialog.accept()
