from repositorio_base import RepositorioBase
from transaccion.modelo import Transaccion
from configuracion.extensiones import db
from base_datos import BaseDatos

class TransaccionRepositorio(RepositorioBase):
    def crear(self, objeto: Transaccion):
        return BaseDatos.agregar(objeto)
    
    def obtener_por_id(self, id_):
        return BaseDatos.obtener_por_id(Transaccion, id_)

    def actualizar(self, objeto: Transaccion):
        return BaseDatos.actualizar(objeto)

    def eliminar(self, id_):
        return BaseDatos.eliminar_por_id(Transaccion, id_)

    def obtener_todos(self, objeto: Transaccion):
        return BaseDatos.obtener_todos(objeto)