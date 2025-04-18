import logging
from modelos.transaccion import Transaccion
from modelos.presupuesto import Presupuesto
from servicios.base_datos import ServicioBaseDatos

class TransaccionServicio:
    @staticmethod
    def registrar_transaccion(cuenta_id, categoria_id, monto):
        presupuesto = ServicioBaseDatos.obtener_unico_con_filtro(Presupuesto, [Presupuesto.categoria_id == categoria_id])
        if not presupuesto:
            error_msg = f"No hay un presupuesto asignado para la categoría {categoria_id}"
            logging.error(error_msg)
            raise Exception(error_msg)
        transaccion = Transaccion(cuenta_id, categoria_id=categoria_id, monto=monto)
        try:
            ServicioBaseDatos.agregar(transaccion)
            presupuesto.monto_gastado += monto
            ServicioBaseDatos.actualizar(presupuesto)
            logging.info("Transacción registrada para categoría %s: monto %s", categoria_id, monto)
        except Exception as e:
            logging.error("Error al registrar transacción para categoría %s: %s", categoria_id, e)
            raise e
        return transaccion

    @staticmethod
    def obtener_transacciones(categoria_id):
        transacciones = ServicioBaseDatos.obtener_con_filtro(Transaccion, [Transaccion.categoria_id == categoria_id])
        logging.info("Obtenidas %d transacciones para la categoría %s", len(transacciones), categoria_id)
        return transacciones

    @staticmethod
    def actualizar_transaccion(transaccion_id, nuevo_monto):
        transaccion = ServicioBaseDatos.obtener_por_id(Transaccion, transaccion_id)
        if transaccion:
            presupuesto = ServicioBaseDatos.obtener_unico_con_filtro(Presupuesto, [Presupuesto.categoria_id == transaccion.categoria_id])
            if presupuesto:
                old_monto = transaccion.monto
                presupuesto.monto_gastado = presupuesto.monto_gastado - old_monto + nuevo_monto
            transaccion.monto = nuevo_monto
            try:
                ServicioBaseDatos.actualizar(transaccion)
                logging.info("Transacción actualizada: ID %s, nuevo monto %s", transaccion_id, nuevo_monto)
            except Exception as e:
                logging.error("Error al actualizar transacción ID %s: %s", transaccion_id, e)
                raise e
        else:
            logging.warning("Transacción no encontrada para actualizar: ID %s", transaccion_id)
        return transaccion

    @staticmethod
    def eliminar_transaccion(transaccion_id):
        transaccion = ServicioBaseDatos.obtener_por_id(Transaccion, transaccion_id)
        if transaccion:
            presupuesto = ServicioBaseDatos.obtener_unico_con_filtro(Presupuesto, [Presupuesto.categoria_id == transaccion.categoria_id])
            if presupuesto:
                presupuesto.monto_gastado -= transaccion.monto
            try:
                ServicioBaseDatos.eliminar(transaccion)
                logging.info("Transacción eliminada: ID %s", transaccion_id)
            except Exception as e:
                logging.error("Error al eliminar transacción ID %s: %s", transaccion_id, e)
                raise e
        else:
            logging.warning("Intento de eliminar transacción inexistente: ID %s", transaccion_id)
        return transaccion
