from modelos.transaccion import Transaccion
from modelos.presupuesto import Presupuesto
from servicios.base_datos import db

class TransaccionServicio:
    @staticmethod
    def registrar_transaccion(categoria_id, monto):
        presupuesto = Presupuesto.query.filter_by(categoria_id=categoria_id).first()
        if not presupuesto:
            raise Exception("No hay un presupuesto asignado para esta categoría")
        transaccion = Transaccion(categoria_id=categoria_id, monto=monto)
        db.session.add(transaccion)
        presupuesto.monto_gastado += monto
        db.session.commit()
        return transaccion

    @staticmethod
    def obtener_transacciones(categoria_id):
        return Transaccion.query.filter_by(categoria_id=categoria_id).all()
