from config import db
from sqlalchemy.orm import relationship, joinedload

class CuentaBancaria(db.Model):
    __tablename__ = 'cuentas_bancarias'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    nombre_banco = db.Column(db.String(100), nullable=False)
    usuario = relationship("Usuario", back_populates="cuentas_bancarias")
    categorias = relationship("Categoria", back_populates="cuenta_bancaria")