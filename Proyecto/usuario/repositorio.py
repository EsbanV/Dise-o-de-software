from repositorio_base import RepositorioBase
from usuario.modelo import Usuario
from configuracion.extensiones import db
from base_datos import BaseDatos

class UsuarioRepositorio(RepositorioBase):
    def crear(self, objeto: Usuario):
        return BaseDatos.agregar(objeto)
    
    def obtener_por_id(self, id_):
        return BaseDatos.obtener_por_id(Usuario, id_)

    def actualizar(self, objeto: Usuario):
        return BaseDatos.actualizar(objeto)

    def eliminar(self, id_):
        return BaseDatos.eliminar_por_id(Usuario, id_)
    
    def obtener_todos(self, objeto: Usuario):
        return BaseDatos.obtener_todos(objeto)
    
    def obtener_usuario_por_correo(self, correo):
        return db.session.query(Usuario).filter_by(correo=correo).first()
    