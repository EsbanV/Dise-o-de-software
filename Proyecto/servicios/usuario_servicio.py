import logging
from configuracion.extensiones import db
from modelos.usuario import Usuario

class UsuarioServicio:

    @staticmethod
    def crear_usuario(nombre, correo, contrasena):
        usuario = Usuario(nombre=nombre, correo=correo, contrasena=contrasena)
        try:
            db.session.add(usuario)
            db.session.commit()
            logging.info("Usuario creado correctamente: %s", correo)
        except Exception as e:
            db.session.rollback()
            logging.error("Error al crear usuario %s: %s", correo, e)
            raise e
        return usuario

    @staticmethod
    def obtener_usuario_por_id(usuario_id):
        return Usuario.query.get(usuario_id)
    
    @staticmethod
    def obtener_usuario_por_correo(correo):
        return Usuario.query.filter_by(correo=correo).first()

    @staticmethod
    def obtener_todos_los_usuarios():
        return Usuario.query.all()

    @staticmethod
    def actualizar_usuario(usuario_id, nombre=None, correo=None, contrasena=None):

        usuario = Usuario.query.get(usuario_id)
        if usuario:
            if nombre:
                usuario.nombre = nombre
            if correo:
                usuario.correo = correo
            if contrasena:
                usuario.contrasena = contrasena
            try:
                db.session.commit()
                logging.info("Usuario actualizado correctamente: %s", usuario_id)
            except Exception as e:
                db.session.rollback()
                logging.error("Error al actualizar usuario %s: %s", usuario_id, e)
                raise e
        return usuario

    @staticmethod
    def eliminar_usuario(usuario_id):

        usuario = Usuario.query.get(usuario_id)
        if usuario:
            try:
                db.session.delete(usuario)
                db.session.commit()
                logging.info("Usuario eliminado: %s", usuario_id)
            except Exception as e:
                db.session.rollback()
                logging.error("Error al eliminar usuario %s: %s", usuario_id, e)
                raise e
            return True
        return False
