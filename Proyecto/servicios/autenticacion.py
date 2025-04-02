from modelos.usuario import Usuario
from servicios.base_datos import ServicioBaseDatos
from utilidades.seguridad import encriptar_contrasena, verificar_contrasena

class ServicioAutenticacion:
    @staticmethod
    def registrar_usuario(nombre, correo, contrasena):
        contrasena_hash = encriptar_contrasena(contrasena)
        nuevo_usuario = Usuario(nombre=nombre, correo=correo, contrasena=contrasena_hash)
        ServicioBaseDatos.agregar(nuevo_usuario)
        return nuevo_usuario

    @staticmethod
    def autenticar_usuario(correo, contrasena):
        usuario = Usuario.query.filter_by(correo=correo).first()
        if usuario and verificar_contrasena(contrasena, usuario.contrasena):
            return usuario
        return None
