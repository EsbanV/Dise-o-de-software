from configuracion import db
from modelos import Usuario

class UsuarioServicio:
    @staticmethod
    def crear_usuario(nombre, correo, contrasena):
        usuario = Usuario(nombre=nombre, correo=correo, contrasena=contrasena)
        db.session.add(usuario)
        db.session.commit()
        return usuario
    
    @staticmethod
    def obtener_usuario_por_id(usuario_id):
        return Usuario.query.get(usuario_id)
    
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
            db.session.commit()
        return usuario
    
    @staticmethod
    def eliminar_usuario(usuario_id):
        usuario = Usuario.query.get(usuario_id)
        if usuario:
            db.session.delete(usuario)
            db.session.commit()
            return True
        return False