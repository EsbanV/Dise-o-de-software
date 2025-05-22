import logging
from modelos.transaccion import Transaccion
from modelos.presupuesto import Presupuesto
from modelos.cuenta_bancaria import CuentaBancaria
from modelos.categoria import TipoCategoria
from sqlalchemy.orm import joinedload
from utilidades.validaciones import validar_monto
from utilidades.validaciones_macro import validar_datos_transaccion
from builder.transaccion_builder import TransaccionBuilder

class TransaccionServicio:
    def __init__(self, repositorio):
        self.repositorio = repositorio

    def registrar_transaccion(self, cuenta_id, categoria_id, descripcion, monto):
        cuenta, categoria = validar_datos_transaccion(
                                self.repositorio,
                                cuenta_id,
                                categoria_id,
                                monto,
                                descripcion=None,
                                fecha=None,
                                validar_saldo=False
                                                     )

        if categoria.tipo == TipoCategoria.GASTO:
            monto = -abs(monto)
        else:
            monto = abs(monto)

        transaccion = (
                TransaccionBuilder()
                .monto(monto)
                .cuenta_bancaria_id(cuenta_id)
                .categoria_id(categoria_id)
                .descripcion(descripcion)
                .build()
            )

        try:
            self.repositorio.agregar(transaccion)
            logging.info("Transacción registrada para categoría %s: monto %s", categoria_id, monto)
        except Exception as e:
            logging.error("Error al registrar transacción para categoría %s: %s", categoria_id, e)
            raise e

        cuenta = self.repositorio.obtener_por_id(CuentaBancaria, cuenta_id)
        cuenta.saldo += monto
        self.repositorio.actualizar()
        logging.info("Saldo de cuenta actualizado: ID %s, nuevo saldo %s", cuenta_id, cuenta.saldo)

        presupuesto = self.repositorio.obtener_unico_con_filtro(Presupuesto, [Presupuesto.categoria_id == categoria_id])
        if presupuesto:
            presupuesto.monto_gastado += monto
            self.repositorio.actualizar()
        else:
            logging.warning("No se encontró presupuesto para la categoría %s", categoria_id)

        return transaccion

    def obtener_transacciones_por_categoria(self, categoria_id):
        transacciones = self.repositorio.obtener_con_filtro(Transaccion, [Transaccion.categoria_id == categoria_id])
        logging.info("Obtenidas %d transacciones para la categoría %s", len(transacciones), categoria_id)
        return transacciones

    def obtener_transacciones_por_cuenta(self, cuenta_id):
        return Transaccion.query.options(
            joinedload(Transaccion.categoria)
        ).filter_by(cuenta_bancaria_id=cuenta_id).all()

    def actualizar_transaccion(self, transaccion_id, nuevo_monto):
        if not validar_monto(nuevo_monto):
            raise ValueError("Monto inválido")

        transaccion = self.repositorio.obtener_por_id(Transaccion, transaccion_id)
        if not transaccion:
            logging.warning("Transacción no encontrada para actualizar: ID %s", transaccion_id)
            return None

        presupuesto = self.repositorio.obtener_unico_con_filtro(Presupuesto, [Presupuesto.categoria_id == transaccion.categoria_id])
        if presupuesto:
            old_monto = transaccion.monto
            presupuesto.monto_gastado = presupuesto.monto_gastado - old_monto + nuevo_monto

        transaccion.monto = nuevo_monto
        try:
            self.repositorio.actualizar(transaccion)
            logging.info("Transacción actualizada: ID %s, nuevo monto %s", transaccion_id, nuevo_monto)
        except Exception as e:
            logging.error("Error al actualizar transacción ID %s: %s", transaccion_id, e)
            raise e
        return transaccion

    def eliminar_transaccion(self, transaccion_id):
        transaccion = self.repositorio.obtener_por_id(Transaccion, transaccion_id)
        if not transaccion:
            logging.warning("Intento de eliminar transacción inexistente: ID %s", transaccion_id)
            return None

        presupuesto = self.repositorio.obtener_unico_con_filtro(Presupuesto, [Presupuesto.categoria_id == transaccion.categoria_id])
        if presupuesto:
            presupuesto.monto_gastado -= transaccion.monto

        try:
            self.repositorio.eliminar(transaccion)
            logging.info("Transacción eliminada: ID %s", transaccion_id)
        except Exception as e:
            logging.error("Error al eliminar transacción ID %s: %s", transaccion_id, e)
            raise e
        return transaccion

    def obtener_por_categoria_y_cuenta(self, cuenta_id, categoria_id):
        return self.repositorio.obtener_con_filtro(
            Transaccion,
            [Transaccion.cuenta_bancaria_id == cuenta_id, Transaccion.categoria_id == categoria_id]
        )
