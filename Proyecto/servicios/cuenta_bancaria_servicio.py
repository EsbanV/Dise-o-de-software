import logging
from modelos.cuenta_bancaria import CuentaBancaria
from servicios.categoria_servicio import CategoriaServicio
from servicios.base_datos import ServicioBaseDatos

class CuentaBancariaServicio:
    @staticmethod
    def crear_cuenta(nombre, saldo_inicial, usuario_id):
        nueva_cuenta = CuentaBancaria(nombre=nombre, saldo=saldo_inicial, usuario_id=usuario_id)
        categorias_gasto = ["Alimentación", "Transporte", "Entretenimiento", "Salud"]
        categorias_ingreso = ["Salario", "Inversiones"]
        try:
            ServicioBaseDatos.agregar(nueva_cuenta)
            for i in categorias_gasto:
                categoria = CategoriaServicio.crear_categoria(i, "GASTO", nueva_cuenta.id)
                ServicioBaseDatos.agregar(categoria)

            for i in categorias_ingreso:
                categoria = CategoriaServicio.crear_categoria(i, "INGRESO", nueva_cuenta.id)
                ServicioBaseDatos.agregar(categoria)

            logging.info("Cuenta bancaria creada correctamente: %s", nueva_cuenta.nombre)
        except Exception as e:
            logging.error("Error al crear cuenta bancaria para usuario %s: %s", usuario_id, e)
            raise e
        return nueva_cuenta

    @staticmethod
    def obtener_cuentas(usuario_id):
        cuentas =   ServicioBaseDatos.obtener_con_filtro(CuentaBancaria, [CuentaBancaria.usuario_id == usuario_id])
        logging.info("Obtenidas %d cuentas para el usuario %s", len(cuentas), usuario_id)
        return cuentas
    
    @staticmethod
    def obtener_cuenta_por_id(cuenta_id):
        cuenta = ServicioBaseDatos.obtener_por_id(CuentaBancaria, cuenta_id)
        if cuenta:
            logging.info("Cuenta bancaria encontrada: ID %s, Nombre %s", cuenta_id, cuenta.nombre)
        else:
            logging.warning("Cuenta bancaria no encontrada: ID %s", cuenta_id)
        return cuenta

    @staticmethod
    def actualizar_cuenta(cuenta_id, nombre=None, saldo=None):
        cuenta = CuentaBancaria.query.get(cuenta_id)
        if cuenta:
            if nombre is not None:
                cuenta.nombre = nombre
            if saldo is not None:
                cuenta.saldo = saldo
            try:
                ServicioBaseDatos.actualizar(cuenta)
                logging.info("Cuenta bancaria actualizada: ID %s", cuenta_id)
            except Exception as e:
                logging.error("Error al actualizar la cuenta ID %s: %s", cuenta_id, e)
                raise e
        else:
            logging.warning("No se pudo actualizar, cuenta no encontrada: ID %s", cuenta_id)
        return cuenta

    @staticmethod
    def eliminar_cuenta(cuenta_id):
        cuenta = CuentaBancaria.query.get(cuenta_id)
        if cuenta:
            try:
                ServicioBaseDatos.eliminar(cuenta)
                logging.info("Cuenta bancaria eliminada: ID %s", cuenta_id)
            except Exception as e:
                logging.error("Error al eliminar cuenta bancaria ID %s: %s", cuenta_id, e)
                raise e
        else:
            logging.warning("Intento de eliminar cuenta inexistente: ID %s", cuenta_id)
        return cuenta
