from typing import Optional

from model.Categoria import Categoria


class Presupuesto:
    def __init__(self,
                 categoria: Categoria,
                 monto_guardado: float,
                 monto_objetivo: float):
        self.categoria = categoria
        self.monto_guardado = monto_guardado
        self.monto_objetivo = monto_objetivo

    def to_dict(self):
        return {
            "categoria": self.categoria.to_dict(),
            "monto_guardado": self.monto_guardado,
            "monto_objetivo": self.monto_objetivo,
        }

    @classmethod
    def from_dict(cls, data):
        categoria = Categoria.from_dict(data["categoria"])
        return cls(
            categoria=categoria,
            monto_guardado=data["monto_guardado"],
            monto_objetivo=data["monto_objetivo"],
        )

    def __repr__(self):
        return (f"categoria={repr(self.categoria)}, "
                f"monto_guardado={self.monto_guardado}, "
                f"monto_objetivo={self.monto_objetivo}")

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

class PresupuestoMensual(PresupuestoPeriodo):
    pass