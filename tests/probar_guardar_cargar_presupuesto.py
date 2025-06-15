from model.Presupuesto import PresupuestoMensual, Presupuesto
from model.PresupuestoRepository import PresupuestoRepository
from model.CategoriaRepository import CategoriaRepository
if __name__ == "__main__":
    repositorio_categoria = CategoriaRepository()
    categorias_egresos = repositorio_categoria.cargar_categorias_egresos()
    lista_presupuestos = []
    for categoria in categorias_egresos:
        presupuesto = Presupuesto(categoria,
                                  monto_guardado=0.0,
                                  monto_objetivo=100.0)
        lista_presupuestos.append(presupuesto)

    # Crear un presupuesto mensual de ejemplo
    presupuesto = PresupuestoMensual("2025-06-01", "2025-06-30", lista_presupuestos)
    repo = PresupuestoRepository()
    usuario = "usuario_prueba"
    mes = "06"
    anio = "2025"

    # Guardar el presupuesto
    repo.guardar_presupuesto_mensual(usuario, mes, anio, presupuesto)
    print("Presupuesto guardado correctamente.")

    # Cargar el presupuesto
    presupuesto_cargado = repo.cargar_presupuesto_mensual(usuario, mes, anio)
    print("Presupuesto cargado:")
    print(presupuesto_cargado.to_dict())

