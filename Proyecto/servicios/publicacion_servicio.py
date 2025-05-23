from modelos.publicacion import Publicacion
from modelos.comentario import Comentario
from observers.observer import NotificationObserver
from flask import abort

class PublicacionService:

    def __init__(self, repositorio, usuario_servicio):
        self.repositorio = repositorio
        self.usuario_servicio = usuario_servicio

    comment_observers = [NotificationObserver()]
    publication_observers  = [NotificationObserver()]
    
    
    def crear_publicacion(self, usuario_id: int, titulo: str, contenido: str) -> Publicacion:
        usuario = self.usuario_servicio.obtener_usuario_activo(usuario_id)
        if not usuario:
            abort(400, description="El usuario está desactivado")

        publicacion = Publicacion(titulo=titulo, contenido=contenido, usuario_id=usuario_id)
        self.repositorio.agregar(publicacion)

        texto = f"{publicacion.usuario.nombre} acaba de publicar «{publicacion.titulo}»"
        for observer in type(self).publication_observers:
            observer.update(publicacion, evento='new_post', mensaje={'mensaje': texto})

        return publicacion
    
    
    def obtener_publicaciones(self):
        return self.repositorio.obtener_todos(Publicacion)

    
    def agregar_comentario(self, publicacion_id: int, usuario_id: int, contenido: str):
        publicacion = self.repositorio.obtener_por_id(Publicacion, publicacion_id)
        if not publicacion:
            abort(404, description="Publicación no encontrada")

        usuario = self.usuario_servicio.obtener_usuario_activo(usuario_id)
        comentario = Comentario(contenido=contenido, usuario_id=usuario_id, publicacion_id=publicacion_id)
        try:
            self.repositorio.agregar(comentario)
            texto = f"{usuario.nombre} comentó en «{publicacion.titulo}»"
            for obs in type(self).comment_observers:
                obs.update(publicacion, evento='comment', mensaje={'mensaje': texto})
        except Exception:
            raise

        return comentario
    
    
    def obtener_publicacion_o_404(self, publicacion_id: int):
        publicacion = self.repositorio.obtener_por_id(Publicacion, publicacion_id)
        if not publicacion:
            abort(404, description="Publicación no encontrada")
        return publicacion
