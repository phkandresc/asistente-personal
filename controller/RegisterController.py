from PyQt6.QtWidgets import QMainWindow, QMessageBox
from model.UserRepository import UserRepository
from utils import Seguridad
from view.RegisterView import Ui_Register
from model.User import User  # Asegúrate de tener esta clase
from utils.Seguridad import hash_password  # Para hashear contraseñas

class RegisterController:
    def __init__(self):
        # Controlador de login (se inicializa después)
        self.login_controller = None
        # Ventana principal para el registro
        self.vista = QMainWindow()
        # Interfaz gráfica de registro
        self.ui = Ui_Register()
        self.ui.setupUi(self.vista)
        # Repositorio para gestionar usuarios
        self.repositorio = UserRepository()
        # Conecta los eventos de la interfaz con sus métodos
        self.conectar_eventos()

    def conectar_eventos(self):
        # Conecta el botón de iniciar sesión con su función
        self.ui.btnIniciarSesion.clicked.connect(self.volver_inicio_sesion)
        # Conecta el botón de registro con su función
        self.ui.btnRegistrarse.clicked.connect(self.registrar_usuario)
        # Conecta el checkbox de mostrar contraseña con su función
        self.ui.cbxMostrarPassword.toggled.connect(self.toggle_password)

    def volver_inicio_sesion(self):
        # Cierra la ventana de registro y abre la de inicio de sesión
        self.vista.close()
        from controller.LoginController import LoginController
        self.login_controller = LoginController()
        self.login_controller.vista.show()

    def toggle_password(self):
        # Alterna la visibilidad de las contraseñas
        if self.ui.cbxMostrarPassword.isChecked():
            self.ui.txtPassword.setEchoMode(self.ui.txtPassword.EchoMode.Normal)
            self.ui.txtConfirmaPassword.setEchoMode(self.ui.txtConfirmaPassword.EchoMode.Normal)
        else:
            self.ui.txtPassword.setEchoMode(self.ui.txtPassword.EchoMode.Password)
            self.ui.txtConfirmaPassword.setEchoMode(self.ui.txtConfirmaPassword.EchoMode.Password)

    def registrar_usuario(self):
        # Obtiene los datos ingresados por el usuario
        nombre = self.ui.txtNombre.text().strip()
        apellido = self.ui.txtApellido.text().strip()
        nombre_usuario = self.ui.txtNombreUsuario.text().strip()
        correo = self.ui.txtCorreo.text().strip()
        password = self.ui.txtPassword.text()
        confirmar_password = self.ui.txtConfirmaPassword.text()

        # Verifica que todos los campos estén completos
        if not all([nombre, apellido, nombre_usuario, correo, password, confirmar_password]):
            QMessageBox.warning(self.vista, "Campos incompletos", "Por favor completa todos los campos.")
            return
        # Verifica que el correo tenga un formato válido
        if not Seguridad.validar_correo(correo):
            QMessageBox.warning(self.vista, "Correo inválido", "Por favor ingresa un correo electrónico válido.")
            return

        # Verifica que las contraseñas coincidan
        if password != confirmar_password:
            QMessageBox.warning(self.vista, "Error de contraseña", "Las contraseñas no coinciden.")
            return

        # Verifica que el nombre de usuario no exista ya
        if self.repositorio.buscar_por_usuario(nombre_usuario):
            QMessageBox.warning(self.vista, "Usuario existente", "El nombre de usuario ya está en uso.")
            return


        # Crea un nuevo usuario
        nuevo_usuario = User(nombre, apellido, nombre_usuario, correo, password)
        # Guarda el usuario en el repositorio
        self.repositorio.registrar_usuario(nuevo_usuario)

        # Muestra mensaje de éxito y vuelve al inicio de sesión
        QMessageBox.information(self.vista, "Registro exitoso", "¡Usuario registrado correctamente!")
        self.volver_inicio_sesion()