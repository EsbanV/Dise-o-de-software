import logging
from presupuesto.modelo import Presupuesto
from presupuesto.repositorio import PresupuestoRepositorio

class PresupuestoServicio:
    _repositorio = PresupuestoRepositorio()

    @staticmethod
    def asignar_presupuesto(categoria_id, monto_asignado):
        try:
            presupuesto = PresupuestoServicio._repositorio.obtener_por_categoria(categoria_id)
            if presupuesto:
                presupuesto.monto_asignado = monto_asignado
                logging.info("Presupuesto actualizado para categoría %s: nuevo monto %s", categoria_id, monto_asignado)
                presupuesto_actualizado = PresupuestoServicio._repositorio.actualizar(presupuesto)
            else:
                nuevo_presupuesto = Presupuesto(categoria_id=categoria_id, monto_asignado=monto_asignado)
                logging.info("Nuevo presupuesto asignado para categoría %s: monto %s", categoria_id, monto_asignado)
                presupuesto_actualizado = PresupuestoServicio._repositorio.crear(nuevo_presupuesto)
            return presupuesto_actualizado
        except Exception as e:
            logging.error("Error al asignar presupuesto para categoría %s: %s", categoria_id, e)
            raise e

    @staticmethod
    def obtener_presupuesto(categoria_id):
        try:
            presupuesto = PresupuestoServicio._repositorio.obtener_por_categoria(categoria_id)
            if presupuesto:
                logging.info("Presupuesto obtenido para categoría %s", categoria_id)
            else:
                logging.info("No se encontró presupuesto para la categoría %s", categoria_id)
            return presupuesto
        except Exception as e:
            logging.error("Error al obtener presupuesto para categoría %s: %s", categoria_id, e)
            raise e

    @staticmethod
    def eliminar_presupuesto(presupuesto_id):
        try:
            presupuesto = PresupuestoServicio._repositorio.eliminar(presupuesto_id)
            if presupuesto:
                logging.info("Presupuesto eliminado: ID %s", presupuesto_id)
            else:
                logging.warning("Intento de eliminar presupuesto inexistente: ID %s", presupuesto_id)
            return presupuesto
        except Exception as e:
            logging.error("Error al eliminar presupuesto ID %s: %s", presupuesto_id, e)
            raise e
