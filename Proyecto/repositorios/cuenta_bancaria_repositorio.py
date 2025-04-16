from repositorios.repositorio_base import RepositorioBase
from modelos.cuenta_bancaria import CuentaBancaria
from configuracion.extensiones import db
from repositorios.base_datos import BaseDatos

class CuentaBancariaRepositorio(RepositorioBase):
    def crear(self, objeto: CuentaBancaria):
        return BaseDatos.agregar(objeto)
    
    def obtener_por_id(self, id_):
        return BaseDatos.obtener_por_id(CuentaBancaria, id_)

    def actualizar(self, objeto: CuentaBancaria):
        return BaseDatos.actualizar(objeto)

    def eliminar(self, id_):
        return BaseDatos.eliminar_por_id(CuentaBancaria, id_)
