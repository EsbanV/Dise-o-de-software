import logging
from modelos.usuario import Usuario
from servicios.base_datos import ServicioBaseDatos
from utilidades.seguridad import encriptar_contrasena, verificar_contrasena
from utilidades.validaciones import validar_email, validar_password

class UsuarioServicio:
    @staticmethod
    def registrar_usuario(nombre, correo, contrasena):
        if validar_email(correo) and validar_password(contrasena):
            
            if ServicioBaseDatos.obtener_con_filtro(Usuario, [Usuario.correo == correo]):
                logging.error("El correo ya está en uso: %s", correo)
                raise ValueError("El correo ya está en uso")

            contrasena = encriptar_contrasena(contrasena)
            usuario = Usuario(nombre=nombre, correo=correo, contrasena=contrasena)
            try:
                ServicioBaseDatos.agregar(usuario)
                logging.info("Usuario creado correctamente: %s", correo)
            except Exception as e:
                logging.error("Error al crear usuario %s: %s", correo, e)
                raise e
            return usuario
        else:
            logging.error("Email inválido: %s", correo)
            raise ValueError("Email inválido")
        
    def iniciar_sesion(correo, contrasena):
        usuario = ServicioBaseDatos.obtener_unico_con_filtro(Usuario, [Usuario.correo == correo])
        if usuario and verificar_contrasena(usuario.contrasena, contrasena):
            logging.info("Inicio de sesión exitoso para: %s", correo)
            return usuario
        else:
            logging.error("Credenciales inválidas para: %s", correo)
            raise ValueError("Credenciales inválidas")

    @staticmethod
    def actualizar_usuario(usuario_id, nombre=None, correo=None, contrasena=None):
        usuario = ServicioBaseDatos.obtener_por_id(Usuario, usuario_id)
        if usuario:
            if nombre:
                usuario.nombre = nombre
            if validar_email(correo):
                usuario.correo = correo
            if validar_password(contrasena):
                usuario.contrasena = encriptar_contrasena(contrasena)
            try:
                ServicioBaseDatos.actualizar(usuario)
                logging.info("Usuario actualizado: ID %s", usuario_id)
            except Exception as e:
                logging.error("Error al actualizar usuario %s: %s", usuario_id, e)
                raise e
        else:
            logging.warning("Usuario no encontrado para actualizar: ID %s", usuario_id)
        return usuario

    @staticmethod
    def eliminar_usuario(usuario_id):
        usuario = Usuario.query.get(usuario_id)
        if usuario:
            try:
                ServicioBaseDatos.eliminar(usuario)
                logging.info("Usuario eliminado: ID %s", usuario_id)
            except Exception as e:
                logging.error("Error al eliminar usuario %s: %s", usuario_id, e)
                raise e
            return True
        logging.warning("Intento de eliminar usuario inexistente: ID %s", usuario_id)
        return False

    def datos_usuario(usuario_id):
        usuario = ServicioBaseDatos.obtener_por_id(Usuario, usuario_id)
        if usuario:
            return usuario
        else:
            logging.warning("Usuario no encontrado: ID %s", usuario_id)
            raise ValueError("Usuario no encontrado")