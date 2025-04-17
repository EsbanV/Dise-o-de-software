from datetime import datetime
from configuracion.extensiones import db

class Transaccion(db.Model):
    __tablename__ = 'transacciones'
    id = db.Column(db.Integer, primary_key=True)
    monto = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)

    def __repr__(self):
        return f'<Transaccion {self.id}>'