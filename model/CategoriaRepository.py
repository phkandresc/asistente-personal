import json
import os
from model.Categoria import Categoria
PATH_CATEGORIAS_INGRESOS = "./data/categorias_ingresos.json"
PATH_CATEGORIAS_EGRESOS = "./data/categorias_egresos.json"


class CategoriaRepository:
    def __init__(self):
        """
        Inicializa el repositorio de categorías.
        Carga las categorías existentes desde el archivo especificado.
        """
        self.categorias_ingresos = self.cargar_categorias_ingresos()
        self.categorias_egresos = self.cargar_categorias_egresos()

    def cargar_categorias_ingresos(self):
        """
        Carga las categorías de ingresos del sistema.
        Retorna una lista de categorías de ingresos.
        """
        if os.path.exists(PATH_CATEGORIAS_INGRESOS) and os.path.getsize(PATH_CATEGORIAS_INGRESOS) > 0:
            with open(PATH_CATEGORIAS_INGRESOS, 'r', encoding='utf-8') as f:
                dic_categorias_ingreso = json.load(f)
                # Convierte cada diccionario de categoría a una instancia de Categoria
                return [Categoria.from_dict(categoria) for categoria in dic_categorias_ingreso]
        else:
            return []

    def cargar_categorias_egresos(self):
        """
        Carga las categorías de egresos del sistema.
        Retorna una lista de categorías de egresos.
        """
        if os.path.exists(PATH_CATEGORIAS_EGRESOS) and os.path.getsize(PATH_CATEGORIAS_EGRESOS) > 0:
            with open(PATH_CATEGORIAS_EGRESOS, 'r', encoding='utf-8') as f:
                dic_categorias_egreso = json.load(f)
                # Convierte cada diccionario de categoría a una instancia de Categoria
                return [Categoria.from_dict(categoria) for categoria in dic_categorias_egreso]
        else:
            return []

    def cargar_categorias_usuario(self, usuario):
        """
        Carga las categorías específicas de un usuario.
        Retorna una lista de categorías asociadas al usuario.
        """
        archivo_categorias_usuario = f"./data/categorias_{usuario.username}.json"
        if os.path.exists(archivo_categorias_usuario) and os.path.getsize(archivo_categorias_usuario) > 0:
            with open(archivo_categorias_usuario, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return []
