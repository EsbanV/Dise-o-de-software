from repositorio_base import RepositorioBase
from categoria.modelo import Categoria
from configuracion.extensiones import db
from base_datos import BaseDatos


class CategoriaRepositorio(RepositorioBase):
    def crear(self, objeto: Categoria):
        return BaseDatos.agregar(objeto)
    
    def obtener_por_id(self, id_):
        return BaseDatos.obtener_por_id(Categoria, id_)

    def actualizar(self, objeto: Categoria):
        return BaseDatos.actualizar(objeto)

    def eliminar(self, id_):
        return BaseDatos.eliminar_por_id(Categoria, id_)
    
    def obtener_todos(self, objeto: Categoria):
        return BaseDatos.obtener_todos(objeto)
