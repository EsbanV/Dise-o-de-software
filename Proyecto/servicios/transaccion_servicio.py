import logging
from modelos.transaccion import Transaccion
from modelos.presupuesto import Presupuesto
from servicios.base_datos import db

class TransaccionServicio:
    @staticmethod
    def registrar_transaccion(categoria_id, monto):
        presupuesto = Presupuesto.query.filter_by(categoria_id=categoria_id).first()
        if not presupuesto:
            error_msg = f"No hay un presupuesto asignado para la categoría {categoria_id}"
            logging.error(error_msg)
            raise Exception(error_msg)
        transaccion = Transaccion(categoria_id=categoria_id, monto=monto)
        try:
            db.session.add(transaccion)
            presupuesto.monto_gastado += monto
            db.session.commit()
            logging.info("Transacción registrada para categoría %s: monto %s", categoria_id, monto)
        except Exception as e:
            db.session.rollback()
            logging.error("Error al registrar transacción para categoría %s: %s", categoria_id, e)
            raise e
        return transaccion

    @staticmethod
    def obtener_transacciones(categoria_id):
        transacciones = Transaccion.query.filter_by(categoria_id=categoria_id).all()
        logging.info("Obtenidas %d transacciones para la categoría %s", len(transacciones), categoria_id)
        return transacciones

    @staticmethod
    def actualizar_transaccion(transaccion_id, nuevo_monto):
        transaccion = Transaccion.query.get(transaccion_id)
        if transaccion:
            presupuesto = Presupuesto.query.filter_by(categoria_id=transaccion.categoria_id).first()
            if presupuesto:
                old_monto = transaccion.monto
                presupuesto.monto_gastado = presupuesto.monto_gastado - old_monto + nuevo_monto
            transaccion.monto = nuevo_monto
            try:
                db.session.commit()
                logging.info("Transacción actualizada: ID %s, nuevo monto %s", transaccion_id, nuevo_monto)
            except Exception as e:
                db.session.rollback()
                logging.error("Error al actualizar transacción ID %s: %s", transaccion_id, e)
                raise e
        else:
            logging.warning("Transacción no encontrada para actualizar: ID %s", transaccion_id)
        return transaccion

    @staticmethod
    def eliminar_transaccion(transaccion_id):
        transaccion = Transaccion.query.get(transaccion_id)
        if transaccion:
            presupuesto = Presupuesto.query.filter_by(categoria_id=transaccion.categoria_id).first()
            if presupuesto:
                presupuesto.monto_gastado -= transaccion.monto
            try:
                db.session.delete(transaccion)
                db.session.commit()
                logging.info("Transacción eliminada: ID %s", transaccion_id)
            except Exception as e:
                db.session.rollback()
                logging.error("Error al eliminar transacción ID %s: %s", transaccion_id, e)
                raise e
        else:
            logging.warning("Intento de eliminar transacción inexistente: ID %s", transaccion_id)
        return transaccion
