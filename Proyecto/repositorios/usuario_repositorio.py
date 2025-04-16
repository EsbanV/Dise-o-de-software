from repositorios.repositorio_base import RepositorioBase
from modelos.usuario import Usuario
from configuracion.extensiones import db
from repositorios.base_datos import BaseDatos

class UsuarioRepositorio(RepositorioBase):
    def crear(self, objeto: Usuario):
        return BaseDatos.agregar(objeto)
    
    def obtener_por_id(self, id_):
        return BaseDatos.obtener_por_id(Usuario, id_)

    def actualizar(self, objeto: Usuario):
        return BaseDatos.actualizar(objeto)

    def eliminar(self, id_):
        return BaseDatos.eliminar_por_id(Usuario, id_)
