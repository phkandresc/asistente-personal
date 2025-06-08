class Categoria:
    # Constructor de la clase Category
    def __init__(self, id: int, nombre: str, descripcion: str = None):
        # Identificador único de la categoría
        self.id = id
        # Nombre de la categoría
        self.nombre = nombre

    def __repr__(self):
        # Representación legible de la categoría para depuración
        return f"Category(id={self.id}, nombre='{self.nombre}')"

    def to_dict(self):
        # Convierte la categoría a un diccionario para almacenamiento o serialización
        return {
            'id': self.id,
            'nombre': self.nombre,
        }

    @classmethod
    def from_dict(cls, data: dict):
        # Crea una instancia de Category a partir de un diccionario
        return cls(
            id=data.get('id'),
            nombre=data.get('nombre'),
        )