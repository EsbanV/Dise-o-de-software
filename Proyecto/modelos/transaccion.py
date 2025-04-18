from datetime import datetime
from configuracion.extensiones import db

class Transaccion(db.Model):
    __tablename__ = 'transacciones'
    id = db.Column(db.Integer, primary_key=True)
    monto = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    cuenta_bancaria_id = db.Column(db.Integer,db.ForeignKey('cuentas_bancarias.id'),  )

    cuenta_bancaria = db.relationship("CuentaBancaria", back_populates="transacciones")
    categoria = db.relationship("Categoria", back_populates="transacciones")

    def __repr__(self):
        return f'<Transaccion {self.id}>'