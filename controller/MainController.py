from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QPushButton, QMainWindow

from controller.PresupuestoController import PresupuestoController
from controller.ResumenController import ResumenController
from controller.TransaccionesController import TransaccionesController
from model.UserRepository import UserRepository

from view.ventanaPrincipal import Ui_ventanaPrincipal


class MainController:
    def __init__(self, usuario):
        self.usuario = usuario

        # Inicializar la ventana principal y su UI
        self.vista = QMainWindow()
        self.ui = Ui_ventanaPrincipal()
        self.ui.setupUi(self.vista)
        self.ui.widgetMenuIconos.hide()
        self.ui.pilaWidgets.setCurrentIndex(0)
        self.ui.btnResumen.setChecked(True)
        self.ui.btnResumen.toggled.connect(lambda: self.cambiar_pagina(0))
        self.ui.btnTransacciones.toggled.connect(lambda: self.cambiar_pagina(1))
        self.ui.btnPresupuesto.toggled.connect(lambda: self.cambiar_pagina(2))
        self.ui.lblUsername.setText(f"Bienvenido, {self.usuario.nombre} {self.usuario.apellido}")

        # Inicializar los controladores de cada pagina
        self.resumen_controller = ResumenController(self.usuario, self.ui)
        self.resumen_controller.cargar_datos()
        self.transacciones_controller = TransaccionesController(self.usuario, self.ui)
        self.presupuesto_controller = PresupuestoController(self.usuario, self.ui)

    def cambiar_pagina(self, index: int):
        self.ui.pilaWidgets.setCurrentIndex(index)
        if index == 0:
            self.resumen_controller.cargar_datos()
        elif index == 1:
            self.transacciones_controller.cargar_datos()
        elif index == 2:
            self.presupuesto_controller.cargar_datos()

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
    repositorio = UserRepository()
    usuario_prueba = repositorio.validar_credenciales("phkandres", "phkandres")
    controlador = MainController(usuario_prueba)
    controlador.vista.show()
    sys.exit(app.exec())
