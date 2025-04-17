import logging
from decimal import Decimal
from utilidades.validadores import validar_id, validar_monto
from utilidades.excepciones import ErrorNegocio, ErrorTecnico
from modelos import Transaccion, Presupuesto
from repositorios.transaccion_repositorio import TransaccionRepositorio
from repositorios.presupuesto_repositorio import PresupuestoRepositorio

class TransaccionServicio:
    _trans_repo = TransaccionRepositorio()
    _presup_repo = PresupuestoRepositorio()

    @staticmethod
    def registrar_transaccion(categoria_id: int, monto: float):
        # Validación inicial
        if not all([validar_id(categoria_id), validar_monto(monto)]):
            raise ErrorNegocio("Datos de transacción inválidos")

        try:
            # Verificar presupuesto existente
            presupuesto = TransaccionServicio._presup_repo.obtener_por_categoria(categoria_id)
            if not presupuesto:
                raise ErrorNegocio("No existe presupuesto para esta categoría")

            # Crear transacción
            nueva_transaccion = Transaccion(
                categoria_id=categoria_id,
                monto=Decimal(str(monto)).quantize(Decimal('0.01'))
            )
            TransaccionServicio._trans_repo.crear(nueva_transaccion)

            # Actualizar presupuesto
            presupuesto.monto_gastado += Decimal(str(monto))
            TransaccionServicio._presup_repo.actualizar(presupuesto)

            return nueva_transaccion

        except ErrorNegocio:
            raise  # Re-lanza errores conocidos
        except Exception as e:
            logging.error(f"Error técnico: {str(e)}", exc_info=True)
            raise ErrorTecnico()

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
