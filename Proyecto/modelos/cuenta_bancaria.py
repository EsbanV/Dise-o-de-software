from configuracion.extensiones import db

class CuentaBancaria(db.Model):
    __tablename__ = 'cuentas_bancarias'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    saldo = db.Column(db.Float, default=0)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    usuario = db.relationship("Usuario", back_populates="cuentas_bancarias")
    
    # Añadir esta relación con Categoria
    categorias = db.relationship('Categoria', backref='cuenta_bancaria', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<CuentaBancaria {self.id}>'