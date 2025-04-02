from config import db
from sqlalchemy.orm import relationship, joinedload

class Categoria(db.Model):
    __tablename__ = 'categorias'
    id = db.Column(db.Integer, primary_key=True)
    cuenta_bancaria_id = db.Column(db.Integer, db.ForeignKey('cuentas_bancarias.id'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    cuenta_bancaria = relationship("CuentaBancaria", back_populates="categorias")
    presupuestos = relationship("Presupuesto", back_populates="categoria")
    transacciones = relationship("Transaccion", back_populates="categoria")
