from config import db
from sqlalchemy.orm import relationship, joinedload
from .categoria import Categoria
from .cuenta_bancaria import CuentaBancaria

class Presupuesto(db.Model):
    __tablename__ = 'presupuestos'
    id = db.Column(db.Integer, primary_key=True)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    gasto_mensual = db.Column(db.Integer, nullable=False)
    saldo_restante = db.Column(db.Integer, nullable=False)
    categoria = relationship("Categoria", back_populates="presupuestos")