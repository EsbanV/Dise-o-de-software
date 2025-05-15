# models/suscripcion_autor.py
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from configuracion.extensiones import db

class SuscripcionAutor(db.Model):
    __tablename__ = 'suscripciones_autor'

    subscriber_id = Column(Integer, ForeignKey('usuarios.id', ondelete='CASCADE'), primary_key=True)
    autor_id      = Column(Integer, ForeignKey('usuarios.id', ondelete='CASCADE'), primary_key=True)
    fecha         = Column(DateTime, default=datetime.utcnow)

    # Relaciones
    suscriptor = relationship("Usuario", foreign_keys=[subscriber_id], back_populates="siguiendo")
    autor      = relationship("Usuario", foreign_keys=[autor_id],      back_populates="seguidores")
