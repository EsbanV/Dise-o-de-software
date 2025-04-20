import logging
from modelos.transaccion import Transaccion
from modelos.presupuesto import Presupuesto
from modelos.cuenta_bancaria import CuentaBancaria
from servicios.base_datos import ServicioBaseDatos
from sqlalchemy.orm import joinedload

class TransaccionServicio:
    @staticmethod
    def registrar_transaccion(cuenta_id, categoria_id, descripcion, monto):
        if not descripcion:
            descripcion = ""

        transaccion = transaccion = Transaccion(cuenta_bancaria_id=cuenta_id, categoria_id=categoria_id, descripcion=descripcion, monto=monto)
        try:
            ServicioBaseDatos.agregar(transaccion)
            logging.info("Transacción registrada para categoría %s: monto %s", categoria_id, monto)
        except Exception as e:
            logging.error("Error al registrar transacción para categoría %s: %s", categoria_id, e)
            raise e
        
        cuenta = ServicioBaseDatos.obtener_por_id(CuentaBancaria, cuenta_id)
        cuenta.saldo += monto
        ServicioBaseDatos.actualizar(cuenta)
        logging.info("Saldo de cuenta actualizado: ID %s, nuevo saldo %s", cuenta_id, cuenta.saldo)
        
        presupuesto = ServicioBaseDatos.obtener_unico_con_filtro(Presupuesto, [Presupuesto.categoria_id == categoria_id])
        if presupuesto:
            presupuesto.monto_gastado += monto
            ServicioBaseDatos.actualizar(presupuesto)
        else:
            logging.warning("No se encontró presupuesto para la categoría %s", categoria_id)
        return transaccion

    @staticmethod
    def obtener_transacciones_por_categoria(categoria_id):
        transacciones = ServicioBaseDatos.obtener_con_filtro(Transaccion, [Transaccion.categoria_id == categoria_id])
        logging.info("Obtenidas %d transacciones para la categoría %s", len(transacciones), categoria_id)
        return transacciones
    
    @staticmethod
    def obtener_transacciones_por_cuenta(cuenta_id):
        return Transaccion.query.options(
            joinedload(Transaccion.categoria)
        ).filter_by(cuenta_bancaria_id=cuenta_id).all()

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

    def obtener_por_categoria_y_cuenta(cuenta_id, categoria_id):
        return ServicioBaseDatos.obtener_con_filtro(Transaccion, [Transaccion.cuenta_bancaria_id == cuenta_id, Transaccion.categoria_id == categoria_id])