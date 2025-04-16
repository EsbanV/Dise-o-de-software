import logging
from modelos.cuenta_bancaria import CuentaBancaria
from repositorios.cuenta_bancaria_repositorio import CuentaBancariaRepositorio

class CuentaBancariaServicio:
    _repositorio = CuentaBancariaRepositorio()

    @staticmethod
    def crear_cuenta(nombre, saldo_inicial, usuario_id):
        if not nombre:
            logging.error("El nombre de la cuenta es requerido.")
            raise ValueError("El nombre de la cuenta es requerido")
        try:
            nueva_cuenta = CuentaBancaria(nombre=nombre, saldo=saldo_inicial, usuario_id=usuario_id)
            cuenta = CuentaBancariaServicio._repositorio.crear(nueva_cuenta)
            logging.info("Cuenta bancaria creada correctamente: %s", cuenta.nombre)
            return cuenta
        except Exception as e:
            logging.error("Error al crear cuenta bancaria para usuario %s: %s", usuario_id, e)
            raise e

    @staticmethod
    def obtener_cuentas(usuario_id):
        try:
            # Se asume que el repositorio tiene un método "obtener_por_usuario"
            cuentas = CuentaBancariaServicio._repositorio.obtener_por_usuario(usuario_id)
            logging.info("Obtenidas %d cuentas para el usuario %s", len(cuentas), usuario_id)
            return cuentas
        except Exception as e:
            logging.error("Error al obtener cuentas para usuario %s: %s", usuario_id, e)
            raise e

    @staticmethod
    def obtener_cuenta_por_id(cuenta_id):
        try:
            cuenta = CuentaBancariaServicio._repositorio.obtener_por_id(cuenta_id)
            if cuenta:
                logging.info("Cuenta bancaria encontrada: ID %s, Nombre %s", cuenta_id, cuenta.nombre)
            else:
                logging.warning("Cuenta bancaria no encontrada: ID %s", cuenta_id)
            return cuenta
        except Exception as e:
            logging.error("Error al obtener cuenta por ID %s: %s", cuenta_id, e)
            raise e

    @staticmethod
    def actualizar_cuenta(cuenta_id, nombre=None, saldo=None):
        cuenta = CuentaBancariaServicio.obtener_cuenta_por_id(cuenta_id)
        if cuenta:
            if nombre is not None:
                cuenta.nombre = nombre
            if saldo is not None:
                cuenta.saldo = saldo
            try:
                cuenta_actualizada = CuentaBancariaServicio._repositorio.actualizar(cuenta)
                logging.info("Cuenta bancaria actualizada: ID %s", cuenta_id)
                return cuenta_actualizada
            except Exception as e:
                logging.error("Error al actualizar la cuenta ID %s: %s", cuenta_id, e)
                raise e
        else:
            logging.warning("No se pudo actualizar, cuenta no encontrada: ID %s", cuenta_id)
        return cuenta

    @staticmethod
    def eliminar_cuenta(cuenta_id):
        try:
            resultado = CuentaBancariaServicio._repositorio.eliminar(cuenta_id)
            if resultado:
                logging.info("Cuenta bancaria eliminada: ID %s", cuenta_id)
            else:
                logging.warning("Intento de eliminar cuenta inexistente: ID %s", cuenta_id)
            return resultado
        except Exception as e:
            logging.error("Error al eliminar cuenta bancaria ID %s: %s", cuenta_id, e)
            raise e
