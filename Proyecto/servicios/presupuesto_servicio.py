import logging
from modelos.presupuesto import Presupuesto
from repositorios.presupuesto_repositorio import PresupuestoRepositorio
from utilidades.validadores import validar_id, validar_monto
from utilidades.excepciones import ErrorNegocio, ErrorTecnico
from decimal import Decimal

class PresupuestoServicio:
    @staticmethod
    def asignar_presupuesto(categoria_id: int, monto_asignado: float):
        # Validación primaria
        if not validar_id(categoria_id) or not validar_monto(monto_asignado):
            raise ErrorNegocio("Datos de presupuesto inválidos.")

        try:
            # Validación de existencia
            from servicios.categoria_servicio import CategoriaServicio
            if not CategoriaServicio.obtener_categoria(categoria_id):
                raise ErrorNegocio("La categoría no existe.")

            # Precisión decimal
            monto = Decimal(str(monto_asignado)).quantize(Decimal('0.01'))

            # Lógica de actualización/creación
            presupuesto = Presupuesto.obtener_por_categoria(categoria_id)
            if presupuesto:
                presupuesto.monto_asignado = monto
            else:
                presupuesto = Presupuesto(categoria_id=categoria_id, monto_asignado=monto)
            
            presupuesto.guardar()
            return presupuesto

        except Exception as e:
            logging.error(f"Error al guardar presupuesto: {str(e)}")
            raise ErrorTecnico()

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
