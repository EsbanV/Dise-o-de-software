import logging
from transaccion.modelo import Transaccion
from transaccion.repositorio import TransaccionRepositorio
from presupuesto.repositorio import PresupuestoRepositorio

class TransaccionServicio:
    _trans_repo = TransaccionRepositorio()
    _presup_repo = PresupuestoRepositorio()

    @staticmethod
    def registrar_transaccion(categoria_id, monto):
        presupuesto = TransaccionServicio._presup_repo.obtener_por_categoria(categoria_id)
        if not presupuesto:
            error_msg = f"No hay un presupuesto asignado para la categoría {categoria_id}"
            logging.error(error_msg)
            raise Exception(error_msg)
        try:
            nueva_transaccion = Transaccion(categoria_id=categoria_id, monto=monto)
            TransaccionServicio._trans_repo.crear(nueva_transaccion)
            presupuesto.monto_gastado += monto
            TransaccionServicio._presup_repo.actualizar(presupuesto)
            logging.info("Transacción registrada para categoría %s: monto %s", categoria_id, monto)
            return nueva_transaccion
        except Exception as e:
            logging.error("Error al registrar transacción para categoría %s: %s", categoria_id, e)
            raise e

    @staticmethod
    def obtener_transacciones(categoria_id):
        try:
            transacciones = TransaccionServicio._trans_repo.obtener_por_categoria(categoria_id)
            logging.info("Obtenidas %d transacciones para la categoría %s", len(transacciones), categoria_id)
            return transacciones
        except Exception as e:
            logging.error("Error al obtener transacciones para categoría %s: %s", categoria_id, e)
            raise e

    @staticmethod
    def actualizar_transaccion(transaccion_id, nuevo_monto):
        transaccion = TransaccionServicio._trans_repo.obtener_por_id(transaccion_id)
        if transaccion:
            presupuesto = TransaccionServicio._presup_repo.obtener_por_categoria(transaccion.categoria_id)
            if presupuesto:
                old_monto = transaccion.monto
                presupuesto.monto_gastado = presupuesto.monto_gastado - old_monto + nuevo_monto
            transaccion.monto = nuevo_monto
            try:
                TransaccionServicio._trans_repo.actualizar(transaccion)
                TransaccionServicio._presup_repo.actualizar(presupuesto)
                logging.info("Transacción actualizada: ID %s, nuevo monto %s", transaccion_id, nuevo_monto)
            except Exception as e:
                logging.error("Error al actualizar transacción ID %s: %s", transaccion_id, e)
                raise e
        else:
            logging.warning("Transacción no encontrada para actualizar: ID %s", transaccion_id)
        return transaccion

    @staticmethod
    def eliminar_transaccion(transaccion_id):
        transaccion = TransaccionServicio._trans_repo.obtener_por_id(transaccion_id)
        if transaccion:
            presupuesto = TransaccionServicio._presup_repo.obtener_por_categoria(transaccion.categoria_id)
            if presupuesto:
                presupuesto.monto_gastado -= transaccion.monto
            try:
                TransaccionServicio._trans_repo.eliminar(transaccion_id)
                TransaccionServicio._presup_repo.actualizar(presupuesto)
                logging.info("Transacción eliminada: ID %s", transaccion_id)
            except Exception as e:
                logging.error("Error al eliminar transacción ID %s: %s", transaccion_id, e)
                raise e
        else:
            logging.warning("Intento de eliminar transacción inexistente: ID %s", transaccion_id)
        return transaccion
