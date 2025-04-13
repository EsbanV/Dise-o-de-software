import logging
from modelos.presupuesto import Presupuesto
from servicios.base_datos import db

class PresupuestoServicio:
    @staticmethod
    def asignar_presupuesto(categoria_id, monto_asignado):
        presupuesto = Presupuesto.query.filter_by(categoria_id=categoria_id).first()
        try:
            if presupuesto:
                presupuesto.monto_asignado = monto_asignado
                logging.info("Presupuesto actualizado para categoría %s: nuevo monto %s", categoria_id, monto_asignado)
            else:
                presupuesto = Presupuesto(categoria_id=categoria_id, monto_asignado=monto_asignado)
                db.session.add(presupuesto)
                logging.info("Nuevo presupuesto asignado para categoría %s: monto %s", categoria_id, monto_asignado)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error("Error al asignar presupuesto para categoría %s: %s", categoria_id, e)
            raise e
        return presupuesto

    @staticmethod
    def obtener_presupuesto(categoria_id):
        presupuesto = Presupuesto.query.filter_by(categoria_id=categoria_id).first()
        if presupuesto:
            logging.info("Presupuesto obtenido para categoría %s", categoria_id)
        else:
            logging.info("No se encontró presupuesto para la categoría %s", categoria_id)
        return presupuesto

    @staticmethod
    def eliminar_presupuesto(presupuesto_id):
        presupuesto = Presupuesto.query.get(presupuesto_id)
        if presupuesto:
            try:
                db.session.delete(presupuesto)
                db.session.commit()
                logging.info("Presupuesto eliminado: ID %s", presupuesto_id)
            except Exception as e:
                db.session.rollback()
                logging.error("Error al eliminar presupuesto ID %s: %s", presupuesto_id, e)
                raise e
        else:
            logging.warning("Intento de eliminar presupuesto inexistente: ID %s", presupuesto_id)
        return presupuesto
