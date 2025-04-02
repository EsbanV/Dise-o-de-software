from config import db
from sqlalchemy.orm import relationship, joinedload
from .categoria import Categoria
from .cuenta_bancaria import CuentaBancaria

class Transaccion(db.Model):
    __tablename__ = 'transacciones'
    id = db.Column(db.Integer, primary_key=True)
    cuenta_bancaria_id = db.Column(db.Integer, db.ForeignKey('cuentas_bancarias.id'), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    presupuesto_id = db.Column(db.Integer, db.ForeignKey('presupuestos.id'), nullable=True)
    descripcion = db.Column(db.String(255), nullable=False)
    fecha = db.Column(db.DateTime, default=db.func.current_timestamp())
    monto = db.Column(db.Integer, nullable=False)
    categoria = relationship("Categoria", back_populates="transacciones")