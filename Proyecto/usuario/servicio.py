import logging
from usuario.modelo import Usuario
from usuario.repositorio import UsuarioRepositorio
from utilidades.validadores import validar_email, validar_password
from utilidades.seguridad import encriptar_contrasena, verificar_contrasena

class UsuarioServicio:
    # Inyectamos el repositorio para desacoplar la persistencia de la lógica del negocio
    _repositorio = UsuarioRepositorio()

    @staticmethod
    def registrar_usuario(nombre, correo, contrasena):

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
    def autenticar_usuario(correo, contrasena):
        usuario = UsuarioServicio._repositorio.obtener_usuario_por_correo(correo)
        if usuario and verificar_contrasena(usuario.contrasena, contrasena):
            return usuario
        return None
    
    @staticmethod
    def ingresar_usuario(usuario_id):
        usuario = UsuarioServicio._repositorio.obtener_por_id(usuario_id)
        if not usuario:
            logging.warning("Usuario no encontrado: ID %s", usuario_id)
            raise ValueError("Usuario no encontrado")
        return usuario