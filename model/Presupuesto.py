from typing import Optional

from model.Categoria import Categoria


class Presupuesto:
    def __init__(self, id_presupuesto,
                 nombre: str,
                 categoria: Categoria,
                 monto_guardado: float,
                 monto_objetivo: float,
                 descripcion: Optional[str] = None):
        self.id_presupuesto = id_presupuesto
        self.nombre = nombre
        self.categoria = categoria
        self.monto_guardado = monto_guardado
        self.monto_objetivo = monto_objetivo
        self.descripcion = descripcion

    def to_dict(self):
        return {
            "id_presupuesto": self.id_presupuesto,
            "nombre": self.nombre,
            "categoria": self.categoria.to_dict(),
            "monto_guardado": self.monto_guardado,
            "monto_objetivo": self.monto_objetivo,
            "descripcion": self.descripcion
        }

    @classmethod
    def from_dict(cls, data):
        categoria = Categoria.from_dict(data["categoria"])
        return cls(
            id_presupuesto=data["id_presupuesto"],
            nombre=data["nombre"],
            categoria=categoria,
            monto_guardado=data["monto_guardado"],
            monto_objetivo=data["monto_objetivo"],
            descripcion=data.get("descripcion")
        )

    def __repr__(self):
        return (f"Presupuesto(id_presupuesto={self.id_presupuesto}, "
                f"nombre='{self.nombre}', "
                f"categoria={repr(self.categoria)}, "
                f"monto_guardado={self.monto_guardado}, "
                f"monto_objetivo={self.monto_objetivo}, "
                f"descripcion={repr(self.descripcion)})")

class PresupuestoPeriodo:
    def __init__(self, fecha_inicio: str, fecha_fin: str, presupuestos: list[Presupuesto]):
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.presupuestos = presupuestos

    def to_dict(self):
        return {
            "fecha_inicio": self.fecha_inicio,
            "fecha_fin": self.fecha_fin,
            "presupuestos": [p.to_dict() for p in self.presupuestos]
        }

    @classmethod
    def from_dict(cls, data):
        presupuestos = [Presupuesto.from_dict(p) for p in data["presupuestos"]]
        return cls(
            fecha_inicio=data["fecha_inicio"],
            fecha_fin=data["fecha_fin"],
            presupuestos=presupuestos
        )

class PresupuestoSemanal(PresupuestoPeriodo):
    pass

class PresupuestoMensual(PresupuestoPeriodo):
    pass