# services/publicacion_service.py
from modelos.publicacion import Publicacion
from modelos.comentario import Comentario
from observers.observer import NotificationObserver
from servicios.base_datos import ServicioBaseDatos
from servicios.usuario_servicio import UsuarioServicio
from servicios.autor_servicio import AutorService
from configuracion.extensiones import db
from flask import abort

class PublicacionService:

    comment_observers = [NotificationObserver()]
    publication_observers  = [NotificationObserver()]
    
    @staticmethod
    def crear_publicacion(usuario_id: int, titulo: str, contenido: str) -> Publicacion:
        usuario = UsuarioServicio.obtener_usuario_activo_por_id(usuario_id)
        if not usuario:
            abort(400, description="El usuario está desactivado")

        publicacion = Publicacion(titulo=titulo, contenido=contenido, usuario_id=usuario_id)
        ServicioBaseDatos.agregar(publicacion)

        texto = f"{publicacion.usuario.nombre} acaba de publicar «{publicacion.titulo}»"
        for observer in PublicacionService.publication_observers:
            observer.update(publicacion, evento='new_post', mensaje={'mensaje': texto})

        return publicacion
    
    @staticmethod
    def obtener_publicaciones():
        return ServicioBaseDatos.obtener_todos(Publicacion)

    @staticmethod
    def agregar_comentario(publicacion_id: int, usuario_id: int, contenido: str):
        publicacion = Publicacion.query.get_or_404(publicacion_id)
        usuario = UsuarioServicio.obtener_usuario_activo_por_id(usuario_id)
        comentario = Comentario(contenido=contenido, usuario_id=usuario_id, publicacion_id=publicacion_id)
        try:
            ServicioBaseDatos.agregar(comentario)
            texto = f"{usuario.nombre} comentó en «{publicacion.titulo}»"
            for obs in PublicacionService.comment_observers:
                obs.update(publicacion, evento='comment', mensaje={'mensaje': texto})
        except Exception:
            raise

        return comentario
    
    @staticmethod
    def obtener_publicacion_o_404(publicacion_id: int):
        publicacion = ServicioBaseDatos.obtener_por_id(Publicacion, publicacion_id)
        if not publicacion:
            abort(404, description="Publicación no encontrada")
        return publicacion
