# controller/LoginController.py

from PyQt6 import QtWidgets
from controller.RegisterController import RegisterController
from model.UserRepository import UserRepository
from PyQt6.QtWidgets import QMessageBox, QMainWindow
from view.LoginView import Ui_Login
from controller.MainController import MainController

class LoginController:
    def __init__(self):
        # Controlador de registro (se inicializa al abrir la ventana de registro)
        self.register_controller = None
        # Ventana principal de login
        self.vista = QMainWindow()
        # Interfaz gráfica de login
        self.ui = Ui_Login()
        self.ui.setupUi(self.vista)
        # Conecta los eventos de la interfaz con sus métodos
        self.conectar_eventos()

    def conectar_eventos(self):
        # Conecta el botón de iniciar sesión con su función
        self.ui.btnIniciarSesion.clicked.connect(self.iniciar_sesion)
        # Conecta el checkbox de mostrar contraseña con su función
        self.ui.cbxMostrarPassword.toggled.connect(self.toggle_password_echo_mode)
        # Conecta el botón de registro con su función
        self.ui.btnRegistrarse.clicked.connect(self.abrir_registro)

    def abrir_registro(self):
        # Cierra la ventana de login y abre la de registro
        self.vista.close()
        self.register_controller = RegisterController()
        self.register_controller.vista.show()

    def toggle_password_echo_mode(self, checked):
        # Alterna la visibilidad de la contraseña
        if checked:
            self.ui.txtPassword.setEchoMode(QtWidgets.QLineEdit.EchoMode.Normal)
        else:
            self.ui.txtPassword.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

    def iniciar_sesion(self):
        # Crea una instancia del repositorio de usuarios
        repositorio = UserRepository()

        # Obtiene los datos ingresados por el usuario
        username = self.ui.txtNombreUsuario.text().strip()
        password = self.ui.txtPassword.text().strip()

        # Verifica que ambos campos estén completos
        if not username or not password:
            QMessageBox.warning(self.vista, "Campos Vacíos", "Por favor, complete todos los campos.")
            return

        # Válida las credenciales con el repositorio
        usuario = repositorio.validar_credenciales(username, password)
        if usuario:
            # Muestra mensaje de bienvenida si las credenciales son correctas
            QMessageBox.information(self.vista, "Bienvenido", f"Hola {usuario.nombre} {usuario.apellido}!")
            # Cierra la ventana de login y abre la ventana principal
            self.vista.close()
            self.main_controller = MainController(usuario)
            self.main_controller.vista.show()
        else:
            # Muestra mensaje de error si las credenciales son incorrectas
            QMessageBox.critical(self.vista, "Error de Inicio de Sesión", "Usuario o contraseña incorrectos.")