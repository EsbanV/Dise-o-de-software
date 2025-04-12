from modelos.cuenta_bancaria import CuentaBancaria
from servicios.base_datos import db

class CuentaBancariaServicio:
    @staticmethod
    def crear_cuenta(nombre, saldo_inicial, usuario_id):
        nueva_cuenta = CuentaBancaria(nombre=nombre, saldo=saldo_inicial, usuario_id=usuario_id)
        db.session.add(nueva_cuenta)
        db.session.commit()
        return nueva_cuenta

    @staticmethod
    def obtener_cuentas(usuario_id):
        return CuentaBancaria.query.filter_by(usuario_id=usuario_id).all()
    
    @staticmethod
    def obtener_cuenta_por_id(cuenta_id):
        return CuentaBancaria.query.get(cuenta_id)

    @staticmethod
    def eliminar_cuenta(cuenta_id):
        cuenta = CuentaBancaria.query.get(cuenta_id)
        if cuenta:
            db.session.delete(cuenta)
            db.session.commit()
        return cuenta
