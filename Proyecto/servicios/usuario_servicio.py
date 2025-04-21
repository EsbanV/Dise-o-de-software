import logging
from modelos.usuario import Usuario
from servicios.base_datos import ServicioBaseDatos
from utilidades.seguridad import encriptar_contrasena, verificar_contrasena
from utilidades.validaciones import validar_datos_usuario, validar_email, validar_password
from servicios.cuenta_bancaria_servicio import CuentaBancariaServicio
from servicios.categoria_servicio import CategoriaServicio
from servicios.transaccion_servicio import TransaccionServicio
from modelos.categoria import TipoCategoria
from modelos.transaccion import Transaccion
from sqlalchemy.orm import joinedload

class UsuarioServicio:

    @staticmethod
    def obtener_usuario_activo_por_id(usuario_id):
        return ServicioBaseDatos.obtener_unico_con_filtro(Usuario, [Usuario.id == usuario_id, Usuario.activo == True])

    @staticmethod
    def registrar_usuario(nombre, correo, contrasena):

        validar_datos_usuario(correo, contrasena)

        if ServicioBaseDatos.obtener_con_filtro(Usuario, [Usuario.correo == correo]):
            logging.error("El correo ya está en uso: %s", correo)
            raise ValueError("El correo ya está en uso")

        usuario = Usuario(nombre=nombre, correo=correo, contrasena=encriptar_contrasena(contrasena))
        try:
            ServicioBaseDatos.agregar(usuario)
            logging.info("Usuario creado correctamente: %s", correo)
        except Exception as e:
            logging.error("Error al crear usuario %s: %s", correo, e)
            raise e
        return usuario

    @staticmethod
    def iniciar_sesion(correo, contrasena):
        usuario = ServicioBaseDatos.obtener_unico_con_filtro(Usuario, [Usuario.correo == correo, Usuario.activo == True])
        if usuario and verificar_contrasena(usuario.contrasena, contrasena):
            logging.info("Inicio de sesión exitoso para: %s", correo)
            return usuario
        else:
            logging.error("Credenciales inválidas para: %s", correo)
            raise ValueError("Credenciales inválidas")

    @staticmethod
    def actualizar_usuario(usuario_id, nombre=None, correo=None, contrasena=None):
        usuario = UsuarioServicio.obtener_usuario_activo_por_id(usuario_id)
        if not usuario:
            logging.warning("Usuario no encontrado para actualizar: ID %s", usuario_id)
            return None

        if nombre:
            usuario.nombre = nombre
        if correo:
            if not validar_email(correo):
                raise ValueError("Email inválido")
            usuario.correo = correo
        if contrasena:
            if not validar_password(contrasena):
                raise ValueError("Contraseña inválida")
            usuario.contrasena = encriptar_contrasena(contrasena)

        try:
            ServicioBaseDatos.actualizar(usuario)
            logging.info("Usuario actualizado: ID %s", usuario_id)
        except Exception as e:
            logging.error("Error al actualizar usuario %s: %s", usuario_id, e)
            raise e
        return usuario

    @staticmethod
    def eliminar_usuario(usuario_id):
        usuario = Usuario.query.get(usuario_id)
        if usuario:
            try:
                usuario.activo = False
                ServicioBaseDatos.actualizar(usuario)
                logging.info("Usuario eliminado: ID %s", usuario_id)
            except Exception as e:
                logging.error("Error al eliminar usuario %s: %s", usuario_id, e)
                raise e
            return True
        logging.warning("Intento de eliminar usuario inexistente: ID %s", usuario_id)
        return False

    @staticmethod
    def datos_usuario(usuario_id):
        usuario = UsuarioServicio.obtener_usuario_activo_por_id(usuario_id)
        if usuario:
            return usuario
        else:
            logging.warning("Usuario no encontrado: ID %s", usuario_id)
            raise ValueError("Usuario no encontrado")

    @staticmethod
    def obtener_resumen(usuario_id, cuenta_id=None):
        usuario = UsuarioServicio.obtener_usuario_activo_por_id(usuario_id)
        if not usuario:
            raise ValueError("Usuario no encontrado o desactivado")

        cuentas = CuentaBancariaServicio.obtener_cuentas(usuario_id)
        if not cuentas:
            return {
                "cuenta": None,
                "cuentas": [],
                "total_ingresos": 0.0,
                "total_gastos": 0.0,
                "categorias": []
            }

        cuenta = next((c for c in cuentas if c.id == cuenta_id), cuentas[0])

        transacciones = Transaccion.query.options(
            joinedload(Transaccion.categoria)
        ).filter_by(cuenta_bancaria_id=cuenta.id).all()

        total_ingresos = sum(
            t.monto for t in transacciones if t.categoria and t.categoria.tipo == TipoCategoria.INGRESO
        )
        total_gastos = sum(
            -t.monto for t in transacciones if t.categoria and t.categoria.tipo == TipoCategoria.GASTO
        )

        categorias_raw = CategoriaServicio.obtener_categorias(cuenta.id)
        categorias = [
            {
                "categoria": cat,
                "transacciones": TransaccionServicio.obtener_por_categoria_y_cuenta(cuenta.id, cat.id)
            }
            for cat in categorias_raw
        ]

        return {
            "cuenta": cuenta,
            "cuentas": cuentas,
            "total_ingresos": total_ingresos,
            "total_gastos": total_gastos,
            "categorias": categorias
        }
    
