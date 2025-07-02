from servicios.base_datos import ServicioBaseDatos
from modelos.publicacion import Publicacion

class PublicacionRepositorio(ServicioBaseDatos):
    
    def obtener_publicaciones(self, limit=5, offset=0):
        print(f"Repositorio: limit={limit}, offset={offset}")
        query = self.session.query(Publicacion).order_by(Publicacion.fecha_creacion.desc())
        total = query.count()
        publicaciones = query.limit(limit).offset(offset).all()
        return publicaciones, total
    
    def obtener_publicaciones_por_usuario(self, usuario_id, limit=5, offset=0):
        print(f"Repositorio: usuario_id{usuario_id} limit={limit}, offset={offset}")
        query = self.session.query(Publicacion).filter(Publicacion.usuario_id == usuario_id).order_by(Publicacion.fecha_creacion.desc())
        total = query.count()
        publicaciones = query.limit(limit).offset(offset).all()
        return publicaciones, total