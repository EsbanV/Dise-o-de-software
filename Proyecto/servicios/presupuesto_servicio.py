from modelos.presupuesto import Presupuesto
from servicios.base_datos import db

class PresupuestoServicio:
    @staticmethod
    def asignar_presupuesto(categoria_id, monto_asignado):
        presupuesto = Presupuesto.query.filter_by(categoria_id=categoria_id).first()
        if presupuesto:
            presupuesto.monto_asignado = monto_asignado
        else:
            presupuesto = Presupuesto(categoria_id=categoria_id, monto_asignado=monto_asignado)
            db.session.add(presupuesto)
        db.session.commit()
        return presupuesto

    @staticmethod
    def obtener_presupuesto(categoria_id):
        return Presupuesto.query.filter_by(categoria_id=categoria_id).first()
