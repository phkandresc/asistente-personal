# model/UserRepository.py

import json
import os
from model.User import User
from utils.Seguridad import verificar_password

class UserRepository:
    """
    Clase responsable de gestionar los usuarios del sistema.
    Permite cargar usuarios desde un archivo JSON, guardar cambios,
    validar credenciales y registrar nuevos usuarios.
    """

    def __init__(self, archivo_usuarios="./data/usuarios.json"):
        """
        Inicializa el repositorio de usuarios.
        Carga los usuarios existentes desde el archivo especificado.
        """
        self.archivo_usuarios = archivo_usuarios
        self.usuarios = self.cargar_usuarios()

    def cargar_usuarios(self):
        """
        Carga la lista de usuarios desde el archivo JSON.
        Si el archivo no existe o está vacío, retorna una lista vacía.
        """
        # Verifica si el archivo existe y no está vacío
        if os.path.exists(self.archivo_usuarios) and os.path.getsize(self.archivo_usuarios) > 0:
            with open(self.archivo_usuarios, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # Si el archivo no existe o está vacío, retorna una lista vacía
            return []

    def guardar_usuarios(self):
        """
        Guarda la lista actual de usuarios en el archivo JSON.
        """
        with open(self.archivo_usuarios, 'w', encoding='utf-8') as f:
            json.dump(self.usuarios, f, indent=4, ensure_ascii=False)

    def validar_credenciales(self, username, password_plana):
        """
        Verifica si las credenciales proporcionadas corresponden a un usuario registrado.
        Retorna el objeto User si las credenciales son válidas, o None en caso contrario.
        """
        print(username, password_plana)
        for usuario in self.usuarios:
            user = User.from_dict(usuario)
            if user.username == username and verificar_password(password_plana, user.password):
                # Si las credenciales son válidas, retorna el objeto User
                print("Credenciales válidas para el usuario:", user.username)  # Depuración
                return user
        print("Credenciales inválidas para el usuario:", username)  # Depuración
        return None


    def registrar_usuario(self, usuario):
        """
        Registra un nuevo usuario si el correo y el nombre de usuario no existen previamente.
        Retorna True si el registro fue exitoso, False si ya existe el usuario o correo.
        """
        # Verifica si el nombre de usuario o el correo ya existen
        if self.buscar_por_usuario(usuario.username) or any(u['email'] == usuario.email for u in self.usuarios):
            return False
        # Agrega el nuevo usuario y guarda los cambios
        self.usuarios.append(usuario.to_dict())
        self.guardar_usuarios()
        return True

    def buscar_por_usuario(self, nombre_usuario):
        """
        Busca un usuario por su nombre de usuario.
        Retorna el objeto User si se encuentra, o None si no existe.
        """
        for usuario in self.usuarios:
            usuario_en_repositorio = User.from_dict(usuario)
            if usuario_en_repositorio.username == nombre_usuario:
                return usuario_en_repositorio
        return None