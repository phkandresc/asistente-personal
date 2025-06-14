import json
import os
from model.Transaccion import Ingreso, Egreso  # Ajusta según tu estructura real

class TransaccionRepository:
    """
    Repositorio para manejar la persistencia de transacciones (ingresos y gastos)
    de diferentes usuarios, utilizando archivos JSON por usuario y tipo.
    """

    def __init__(self, base_path=None):
        if base_path is None:
            base_dir = os.path.abspath(os.path.dirname(__file__))
            base_path = os.path.join(base_dir, "../data/usuarios")
        self.base_path = base_path

    def _normalizar_tipo(self, tipo: str) -> str:
        """
        Normaliza el tipo de transacción a 'ingresos' o 'egresos'.
        """
        if tipo.lower() in ["ingreso", "ingresos"]:
            return "ingresos"
        elif tipo.lower() in ["egreso", "egresos"]:
            return "egresos"
        return tipo

    def obtener_ruta_usuario(self, username: str, tipo: str) -> str:
        user_dir = os.path.join(self.base_path, username)
        tipo = self._normalizar_tipo(tipo)
        return os.path.join(user_dir, f"{tipo}.json")

    def cargar_transacciones(self, username: str, tipo: str) -> list:
        ruta_usuario = self.obtener_ruta_usuario(username, tipo)
        print(os.path.exists(ruta_usuario))
        print(ruta_usuario)
        if os.path.exists(ruta_usuario) and os.path.getsize(ruta_usuario) > 0:
            with open(ruta_usuario, 'r', encoding='utf-8') as f:
                transacciones = json.load(f)
                tipo_norm = self._normalizar_tipo(tipo)
                return [Ingreso.from_dict(t) if tipo_norm == "ingresos" else Egreso.from_dict(t) for t in transacciones]
        return []

    def guardar_transacciones(self, username: str, tipo: str, transacciones: list):
        path = self.obtener_ruta_usuario(username, tipo)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump([t.to_dict() for t in transacciones], f, indent=4, ensure_ascii=False)

    def obtener_nuevo_id(self, username: str, tipo: str) -> int:
        transacciones = self.cargar_transacciones(username, tipo)
        if transacciones:
            return max(t.id for t in transacciones) + 1
        return 1

    def registrar_transaccion(self, username: str, transaccion):
        tipo = "ingresos" if isinstance(transaccion, Ingreso) else "egresos"
        transacciones = self.cargar_transacciones(username, tipo)
        transacciones.append(transaccion)
        self.guardar_transacciones(username, tipo, transacciones)

    def egresos_por_dia(self, username: str) -> dict:
        from collections import defaultdict
        egresos = self.cargar_transacciones(username, "egresos")
        gastos_por_fecha = defaultdict(float)
        for e in egresos:
            fecha = getattr(e, 'fecha', None)
            monto = getattr(e, 'monto', 0)
            if fecha:
                gastos_por_fecha[fecha] += monto
        return dict(gastos_por_fecha)

    def cargar_transacciones_por_dia(self, username: str, tipo: str, fecha: str) -> list:
        transacciones = self.cargar_transacciones(username, tipo)
        return [t for t in transacciones if getattr(t, 'fecha', None) == fecha]

    def actualizar_transaccion(self, username: str, tipo: str, transaccion_actualizada) -> bool:
        tipo = self._normalizar_tipo(tipo)
        transacciones = self.cargar_transacciones(username, tipo)
        print("en metodo actualizar transaccion")
        print(transaccion_actualizada)
        for idx, t in enumerate(transacciones):
            if getattr(t, 'id', None) == getattr(transaccion_actualizada, 'id', None):
                transacciones[idx] = transaccion_actualizada
                self.guardar_transacciones(username, tipo, transacciones)
                return True
        return False
