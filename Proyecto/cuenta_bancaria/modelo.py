from configuracion.extensiones import db

class CuentaBancaria(db.Model):
    __tablename__ = 'cuenta_bancaria'

    id         = db.Column(db.Integer, primary_key=True)
    nombre     = db.Column(db.String(100), nullable=False)
    saldo      = db.Column(db.Float, default=0)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    usuario = db.relationship('Usuario', back_populates='cuentas_bancarias')
    categorias = db.relationship('Categoria', back_populates='cuenta_bancaria')

    def depositar(self, monto: float) -> None:
        self.saldo += monto

    def retirar(self, monto: float) -> bool:
        if self.saldo >= monto:
            self.saldo -= monto
            return True
        return False

