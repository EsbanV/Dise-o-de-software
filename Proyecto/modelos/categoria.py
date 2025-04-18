from configuracion.extensiones import db
from enum import Enum
from sqlalchemy import Enum as SqlEnum

class TipoCategoria(Enum):
    INGRESO = "ingreso"
    GASTO = "gasto"

class Categoria(db.Model):
    __tablename__ = 'categorias'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    tipo = db.Column(SqlEnum(TipoCategoria), nullable=False)
    cuenta_id = db.Column(db.Integer, db.ForeignKey('cuentas_bancarias.id'), nullable=False)

    cuenta_bancaria = db.relationship("CuentaBancaria", back_populates="categorias")
    presupuesto = db.relationship("Presupuesto", uselist=False, back_populates="categoria")
    transacciones = db.relationship("Transaccion", back_populates="categoria")

    def es_ingreso(self):
        return self.tipo == TipoCategoria.INGRESO

    def es_gasto(self):
        return self.tipo == TipoCategoria.GASTO

    def __repr__(self):
        return f'<Categoria {self.id} - {self.nombre}>'