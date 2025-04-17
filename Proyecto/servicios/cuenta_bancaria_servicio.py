import logging
from modelos.cuenta_bancaria import CuentaBancaria
from repositorios.cuenta_bancaria_repositorio import CuentaBancariaRepositorio
from servicios.usuario_servicio import UsuarioServicio
from utilidades.validadores import validar_nombre, validar_monto, validar_id
from utilidades.validadores import validar_nombre, validar_monto, validar_id
from utilidades.excepciones import ErrorNegocio, ErrorTecnico
from decimal import Decimal
from sqlalchemy.exc import SQLAlchemyError
from configuracion.extensiones import db

class CuentaBancariaServicio:
    _repositorio = CuentaBancariaRepositorio()

    @classmethod
    def crear_cuenta(cls, nombre: str, saldo_inicial: float, usuario_id: int):
        try:
            # Validaciones
            if not validar_nombre(nombre):
                raise ErrorNegocio("Nombre inválido")
            
            if not validar_monto(saldo_inicial):
                raise ErrorNegocio("Saldo inválido")
                
            if not validar_id(usuario_id):
                raise ErrorNegocio("Usuario inválido")

            # Verificar existencia del usuario
            if not UsuarioServicio.obtener_usuario_por_id(usuario_id):
                raise ErrorNegocio("El usuario no existe")

            # Creación
            cuenta = CuentaBancaria(
                nombre=nombre.strip(),
                saldo=Decimal(str(saldo_inicial)).quantize(Decimal('0.01')),
                usuario_id=usuario_id
            )
            
            # Guardado con manejo explícito de errores SQL
            try:
                db.session.add(cuenta)
                db.session.commit()
                return cuenta
            except SQLAlchemyError as e:
                db.session.rollback()
                logging.error(f"Error de BD al crear cuenta: {str(e)}")
                raise ErrorTecnico("Error al guardar en base de datos")
                
        except ErrorNegocio:
            raise  # Re-lanza errores de negocio
        except Exception as e:
            logging.critical(f"Error inesperado: {str(e)}", exc_info=True)
            raise ErrorTecnico()
    @classmethod
    def obtener_cuentas(cls, usuario_id: int):
        """Obtiene todas las cuentas de un usuario"""
        try:
            if not usuario_id:
                raise ValueError("ID de usuario requerido")
                
            cuentas = cls._repositorio.obtener_por_usuario(usuario_id)
            logging.info(f"Obtenidas {len(cuentas)} cuentas para usuario {usuario_id}")
            return cuentas
        except Exception as e:
            logging.error(f"Error al obtener cuentas: {str(e)}")
            return []  # Retorna lista vacía en caso de error

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
