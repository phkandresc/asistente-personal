import json
import os
from typing import List, Union
from model.Presupuesto import Presupuesto
from model.Presupuesto import PresupuestoSemanal
from model.Presupuesto import PresupuestoMensual

class PresupuestoRepository:
    def __init__(self, base_path="./data/usuarios"):
        self.base_path = base_path

    def _get_presupuesto_path(self, usuario: str, tipo: str, identificador: str) -> str:
        """
        Construye la ruta del archivo donde se guarda el presupuesto.
        tipo: 'semanal' o 'mensual'
        identificador: puede ser '2025-06-03' para semanal o '2025-06' para mensual
        """
        user_dir = os.path.join(self.base_path, usuario, "presupuestos")
        os.makedirs(user_dir, exist_ok=True)
        return os.path.join(user_dir, f"{tipo}_{identificador}.json")

    def guardar_presupuesto(self, usuario: str, presupuesto: Union[PresupuestoSemanal, PresupuestoMensual], tipo: str, identificador: str):
        """
        Guarda un presupuesto semanal o mensual en archivo.
        """
        ruta = self._get_presupuesto_path(usuario, tipo, identificador)
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(presupuesto.to_dict(), f, indent=4, ensure_ascii=False)

    def cargar_presupuesto(self, usuario: str, tipo: str, identificador: str) -> Union[PresupuestoSemanal, PresupuestoMensual, None]:
        """
        Carga un presupuesto desde archivo. Devuelve None si no existe.
        """
        ruta = self._get_presupuesto_path(usuario, tipo, identificador)
        if not os.path.exists(ruta):
            return None

        with open(ruta, "r", encoding="utf-8") as f:
            data = json.load(f)

        if tipo == "semanal":
            return PresupuestoSemanal.from_dict(data)
        elif tipo == "mensual":
            return PresupuestoMensual.from_dict(data)
        else:
            raise ValueError("Tipo de presupuesto no válido. Usa 'semanal' o 'mensual'.")

    def listar_presupuestos(self, usuario: str) -> list[str]:
        """
        Lista todos los archivos de presupuesto de un usuario.
        """
        presupuestos_dir = os.path.join(self.base_path, usuario, "presupuestos")
        if not os.path.exists(presupuestos_dir):
            return []
        return [f for f in os.listdir(presupuestos_dir) if f.endswith(".json")]
