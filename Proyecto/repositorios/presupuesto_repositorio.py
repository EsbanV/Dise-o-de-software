from repositorios.repositorio_base import RepositorioBase
from modelos.presupuesto import Presupuesto
from configuracion.extensiones import db
from repositorios.base_datos import BaseDatos

class PresupuestoRepositorio(RepositorioBase):
    def crear(self, objeto: Presupuesto):
        return BaseDatos.agregar(objeto)
    
    def obtener_por_id(self, id_):
        return BaseDatos.obtener_por_id(Presupuesto, id_)

    def actualizar(self, objeto: Presupuesto):
        return BaseDatos.actualizar(objeto)

    def eliminar(self, id_):
        return BaseDatos.eliminar_por_id(Presupuesto, id_)
