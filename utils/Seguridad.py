import hashlib
import re

def hash_password(password):
    """Devuelve el hash SHA-256 de una contraseña."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def verificar_password(password_plana, password_hash):
    """Verifica si el hash de una contraseña coincide con uno almacenado."""
    return hash_password(password_plana) == password_hash

def validar_correo(correo):
    """Valida el formato de un correo electrónico simple."""
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(patron, correo) is not None