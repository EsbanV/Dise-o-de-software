import logging
from modelos.usuario import Usuario
from repositorios.usuario_repositorio import UsuarioRepositorio
from utilidades.validadores import validar_email, validar_password
from utilidades.seguridad import encriptar_contrasena

class UsuarioServicio:
    # Inyectamos el repositorio para desacoplar la persistencia de la lógica del negocio
    _repositorio = UsuarioRepositorio()

    @staticmethod
    def crear_usuario(nombre, correo, contrasena):
        if not validar_email(correo):
            logging.error("El correo %s no es válido", correo)
            raise ValueError("El correo no es válido")
        if not validar_password(contrasena):
            logging.error("La contraseña no cumple los criterios mínimos")
            raise ValueError("La contraseña no cumple los requisitos")

        usuario_existente = UsuarioServicio._repositorio.obtener_usuario_por_correo(correo)
        if usuario_existente:
            logging.warning("El correo %s ya se encuentra registrado", correo)
            raise ValueError("El correo ya está registrado")

        contrasena_hash = encriptar_contrasena(contrasena)
        nuevo_usuario = Usuario(nombre=nombre, correo=correo, contrasena=contrasena_hash)
        try:
            usuario_creado = UsuarioServicio._repositorio.crear(nuevo_usuario)
            logging.info("Usuario creado correctamente: %s", correo)
            return usuario_creado
        except Exception as e:
            logging.error("Error al crear usuario %s: %s", correo, e)
            raise e

    @staticmethod
    def obtener_usuario_por_id(usuario_id):
        usuario = UsuarioServicio._repositorio.obtener_por_id(usuario_id)
        logging.info("Obtenido usuario por ID: %s", usuario_id)
        return usuario

    @staticmethod
    def obtener_usuario_por_correo(correo):
        usuario = UsuarioServicio._repositorio.obtener_por_correo(correo)
        if usuario:
            logging.info("Usuario encontrado por correo: %s", correo)
        else:
            logging.info("No se encontró usuario con el correo: %s", correo)
        return usuario

    @staticmethod
    def obtener_todos_los_usuarios():
        usuarios = UsuarioServicio._repositorio.obtener_todos()
        logging.info("Obtenidos %d usuarios en total", len(usuarios))
        return usuarios

    @staticmethod
    def actualizar_usuario(usuario_id, nombre=None, correo=None, contrasena=None):
        usuario = UsuarioServicio._repositorio.obtener_por_id(usuario_id)
        if usuario:
            if nombre:
                usuario.nombre = nombre
            if correo:
                if not validar_email(correo):
                    logging.error("El correo %s no es válido", correo)
                    raise ValueError("El correo no es válido")
                
                usuario_existente = UsuarioServicio._repositorio.obtener_usuario_por_correo(correo)

                if usuario_existente:
                    logging.warning("El correo %s ya se encuentra registrado", correo)
                    raise ValueError("El correo ya está registrado")
                usuario.correo = correo

            if contrasena:
                if not validar_password(contrasena):
                    logging.error("La contraseña no cumple con los criterios")
                    raise ValueError("La contraseña no es válida")
                usuario.contrasena = encriptar_contrasena(contrasena)
            try:
                usuario_actualizado = UsuarioServicio._repositorio.actualizar(usuario)
                logging.info("Usuario actualizado: ID %s", usuario_id)
                return usuario_actualizado
            except Exception as e:
                logging.error("Error al actualizar usuario %s: %s", usuario_id, e)
                raise e
        else:
            logging.warning("Usuario no encontrado para actualizar: ID %s", usuario_id)
        return usuario

    @staticmethod
    def eliminar_usuario(usuario_id):
        try:
            resultado = UsuarioServicio._repositorio.eliminar(usuario_id)
            if resultado:
                logging.info("Usuario eliminado: ID %s", usuario_id)
                return True
            else:
                logging.warning("Intento de eliminar usuario inexistente: ID %s", usuario_id)
                return False
        except Exception as e:
            logging.error("Error al eliminar usuario %s: %s", usuario_id, e)
            raise e
