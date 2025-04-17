from configuracion.extensiones import db

class Categoria(db.Model):
    __tablename__ = 'categoria'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    cuenta_id = db.Column(db.Integer, db.ForeignKey('cuenta_bancaria.id'), nullable=False)
    cuenta_bancaria = db.relationship('CuentaBancaria', back_populates='categorias')

    def es_ingreso(self) -> bool:
        if self.tipo == 'Ingreso':
            return True
        return False

    def signo(self) -> int:
        if self.tipo == 'Ingreso':
            return 1
        return -1
