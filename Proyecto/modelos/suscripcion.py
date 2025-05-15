# models.py (o donde agrupes tus modelos)
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from datetime import datetime
from configuracion.extensiones import db

class Suscripcion(db.Model):
    __tablename__ = 'suscripciones'

    # Clave primaria compuesta
    usuario_id     = Column(Integer, ForeignKey('usuarios.id', ondelete='CASCADE'), primary_key=True)
    publicacion_id = Column(Integer, ForeignKey('publicaciones.id', ondelete='CASCADE'), primary_key=True)

    # Campos adicionales
    fecha           = Column(DateTime, default=datetime.utcnow)
    estado          = Column(String(20), default='activa')

    # Relaciones de navegación
    usuario     = relationship("Usuario",      back_populates="suscripciones")
    publicacion = relationship("Publicacion",  back_populates="suscripciones")
