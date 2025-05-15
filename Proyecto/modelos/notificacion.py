from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from configuracion.extensiones import db

class Notificacion(db.Model):
    __tablename__ = 'notificaciones'

    id = Column(Integer, primary_key=True)
    mensaje = Column(String(255), nullable=False)
    leida = Column(Boolean, default=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    # Relaciones
    usuario_id = Column(Integer, ForeignKey('usuarios.id', ondelete='CASCADE'))
    usuario = relationship("Usuario", back_populates="notificaciones")

    def __repr__(self):
        return f'<Notificación {self.mensaje} para Usuario {self.usuario_id}>'
