import json
import os

from model.Transaccion import Ingreso, Egreso  # Ajusta según tu estructura real

class TransaccionRepository:
    """
    Repositorio para manejar la persistencia de transacciones (ingresos y gastos)
    de diferentes usuarios, utilizando archivos JSON por usuario y tipo.
    """

    def __init__(self, base_path="./data/usuarios"):
        """
        Inicializa el repositorio con la ruta base donde se almacenan los datos de usuarios.
        """
        self.base_path = base_path

    def obtener_ruta_usuario(self, username: str, tipo: str) -> str:
        """
        Retorna la ruta del archivo JSON para un usuario y tipo de transacción.
        """
        user_dir = os.path.join(self.base_path, username)
        return os.path.join(user_dir, f"{tipo}.json")  # tipo: ingresos o gastos

    def cargar_transacciones(self, username: str, tipo: str) -> list:
        """
        Carga y retorna la lista de transacciones del tipo dado (ingresos/gastos)
        para el usuario especificado. Si el archivo no existe o está vacío, retorna una lista vacía.
        """
        ruta_usuario = self.obtener_ruta_usuario(username, tipo)
        print(os.path.exists(ruta_usuario))
        print(ruta_usuario)
        if os.path.exists(ruta_usuario) and os.path.getsize(ruta_usuario) > 0:
            with open(ruta_usuario, 'r', encoding='utf-8') as f:
                transacciones = json.load(f)
                return [Ingreso.from_dict(t) if tipo == "ingresos" else Egreso.from_dict(t) for t in transacciones]
        return []

    def guardar_transacciones(self, username: str, tipo: str, transacciones: list):
        """
        Guarda la lista de transacciones en el archivo correspondiente al usuario y tipo.
        """
        path = self.obtener_ruta_usuario(username, tipo)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump([t.to_dict() for t in transacciones], f, indent=4, ensure_ascii=False)

    def obtener_nuevo_id(self, username: str, tipo: str) -> int:
        """
        Calcula y retorna un nuevo ID incremental para una transacción del tipo y usuario dado.
        Si no hay transacciones previas, retorna 1.
        """
        transacciones = self.cargar_transacciones(username, tipo)
        if transacciones:
            return max(t.id for t in transacciones) + 1
        return 1

    def registrar_transaccion(self, username: str, transaccion):
        """
        Registra una transacción (Ingreso o Egreso) para un usuario específico.
        Determina el tipo, la agrega a la lista y la guarda en el archivo correspondiente.
        """
        tipo = "ingresos" if isinstance(transaccion, Ingreso) else "egresos"
        transacciones = self.cargar_transacciones(username, tipo)
        transacciones.append(transaccion)
        self.guardar_transacciones(username, tipo, transacciones)
