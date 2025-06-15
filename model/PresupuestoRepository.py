import json
import os
from model.Presupuesto import Presupuesto, PresupuestoMensual

class PresupuestoRepository:
    def __init__(self, base_path=None):
        if base_path is None:
            base_dir = os.path.abspath(os.path.dirname(__file__))
            base_path = os.path.join(base_dir, "../data/usuarios")
        self.base_path = base_path

    def crear_directorio_presupuesto(self, username: str):
        """
        Crea un directorio 'presupuestos' dentro de la carpeta del usuario.
        """
        directorio_usuario = os.path.join(self.base_path, username)
        directorio_presupuestos = os.path.join(directorio_usuario, "presupuestos")
        if not os.path.exists(directorio_presupuestos):
            os.makedirs(directorio_presupuestos)
        return directorio_presupuestos

    def obtener_ruta_presupuesto_mensual(self, username: str, mes: str, anio: str) -> str:
        """
        Obtiene la ruta del archivo de presupuesto mensual para un usuario y mes específicos.
        """
        directorio_presupuestos = self.crear_directorio_presupuesto(username)
        return os.path.join(directorio_presupuestos, f"presupuesto_{anio}-{mes}.json")

    def guardar_presupuesto_mensual(self, username: str, mes: str, anio: str, presupuesto: PresupuestoMensual):
        """
        Guarda un objeto PresupuestoMensual como archivo JSON en la ruta correspondiente.
        """
        ruta_archivo = self.obtener_ruta_presupuesto_mensual(username, mes, anio)
        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            json.dump(presupuesto.to_dict(), f, ensure_ascii=False, indent=4)

    def cargar_presupuesto_mensual(self, username: str, mes: str, anio: str) -> PresupuestoMensual:
        """
        Carga un objeto PresupuestoMensual desde el archivo JSON correspondiente y actualiza el monto guardado de cada categoría.
        Lanza FileNotFoundError si el archivo no existe.
        """
        ruta_archivo = self.obtener_ruta_presupuesto_mensual(username, mes, anio)
        if not os.path.exists(ruta_archivo):
            raise FileNotFoundError(f"No existe el presupuesto para {username} en {mes}/{anio}")
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            data = json.load(f)
        presupuesto = PresupuestoMensual.from_dict(data)
        # Actualizar monto_guardado de cada categoría usando TransaccionRepository
        from model.TransaccionRepository import TransaccionRepository
        trans_repo = TransaccionRepository()
        totales_por_categoria = trans_repo.obtener_egresos_por_usuario_y_mes(username, mes, anio)
        for p in presupuesto.presupuestos:
            p.monto_guardado = totales_por_categoria.get(p.categoria.id, 0)
        return presupuesto

    def eliminar_categoria_presupuesto_mensual(self, username: str, mes: str, anio: str, categoria_id: str):
        """
        Elimina una categoría del presupuesto mensual del usuario.
        """
        try:
            presupuesto = self.cargar_presupuesto_mensual(username, mes, anio)
            presupuesto.presupuestos = [p for p in presupuesto.presupuestos if p.categoria.id != categoria_id]
            self.guardar_presupuesto_mensual(username, mes, anio, presupuesto)
        except FileNotFoundError:
            raise FileNotFoundError(f"No existe el presupuesto para {username} en {mes}/{anio}")
