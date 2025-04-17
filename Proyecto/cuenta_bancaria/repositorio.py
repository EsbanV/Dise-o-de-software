from repositorio_base import RepositorioBase
from cuenta_bancaria.modelo import CuentaBancaria
from configuracion.extensiones import db
from base_datos import BaseDatos

class CuentaBancariaRepositorio(RepositorioBase):
    def crear(self, objeto: CuentaBancaria):
        return BaseDatos.agregar(objeto)
    
    def obtener_por_id(self, id_):
        return BaseDatos.obtener_por_id(CuentaBancaria, id_)

    def actualizar(self, objeto: CuentaBancaria):
        return BaseDatos.actualizar(objeto)

    def eliminar(self, id_):
        return BaseDatos.eliminar_por_id(CuentaBancaria, id_)

    def obtener_todos(self, objeto: CuentaBancaria):
        return BaseDatos.obtener_todos(objeto)
    
    def obtener_por_usuario(self, usuario_id):
        return db.session.query(CuentaBancaria).filter_by(usuario_id=usuario_id).all()