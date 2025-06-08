# Importa tipos para anotaciones y la clase Category
from typing import Optional, Any
from model.Categoria import Categoria

# Clase base para representar una transacción financiera genérica
class Transaccion:
    def __init__(self, id: int, monto: float, fecha: str, categoria: Categoria, descripcion: Optional[str] = None):
        # Inicializa los atributos de la transacción
        self.id = id  # Identificador único de la transacción
        self.monto = monto  # Monto de la transacción
        self.fecha = fecha  # Fecha en formato 'YYYY-MM-DD'
        self.categoria = categoria  # Categoría asociada (objeto Category)
        self.descripcion = descripcion  # Descripción opcional

    def __repr__(self):
        # Representación en cadena de la instancia para depuración
        return (f"{self.__class__.__name__}(id={self.id}, monto={self.monto}, fecha='{self.fecha}', "
                f"categoria={repr(self.categoria)}, descripcion={repr(self.descripcion)})")

    def to_dict(self):
        # Convierte la instancia en un diccionario serializable
        return {
            'id': self.id,
            'monto': self.monto,
            'fecha': self.fecha,
            'categoria': self.categoria.to_dict(),  # Serializa la categoría
            'descripcion': self.descripcion,
            'tipo': self.__class__.__name__.lower()  # Tipo de transacción en minúsculas
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Transaccion":
        # Crea una instancia de Transaccion a partir de un diccionario
        categoria_data = data['categoria']
        categoria = Categoria.from_dict(categoria_data)  # Deserializa la categoría
        return cls(
            id=data['id'],
            monto=data['monto'],
            fecha=data['fecha'],
            categoria=categoria,
            descripcion=data.get('descripcion')
        )

# Subclase que representa un ingreso
class Ingreso(Transaccion):
    pass

# Subclase que representa un gasto
class Egreso(Transaccion):
    pass