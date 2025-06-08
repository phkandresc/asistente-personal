# Clase que representa un usuario del sistema
from utils.Seguridad import hash_password

class User:
    def __init__(self, nombre, apellido, username, email, password, hashed=False):
        # Inicializa los atributos del usuario
        self.nombre = nombre.title()  # Capitaliza el nombre
        self.apellido = apellido.title()  # Capitaliza el apellido
        self.username = username
        self.email = email
        # Si la contraseña no está hasheada, la hashea
        self.password = password if hashed else hash_password(password)

    def __repr__(self):
        # Representación legible del usuario para depuración
        return f"User(username='{self.username}', email='{self.email}')"

    def to_dict(self):
        # Convierte el usuario a un diccionario para almacenamiento o serialización
        return {
            'nombre': self.nombre,
            'apellido': self.apellido,
            'username': self.username,
            'email': self.email,
            'password': self.password
        }

    @classmethod
    def from_dict(cls, data):
        # Crea una instancia de User a partir de un diccionario
        return cls(
            nombre=data.get('nombre'),
            apellido=data.get('apellido'),
            username=data.get('username'),
            email=data.get('email'),
            password=data.get('password'),
            hashed=True  # Indica que la contraseña ya está hasheada
        )