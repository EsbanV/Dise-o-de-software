from configuracion.extensiones import db

class Categoria(db.Model):
    __tablename__ = 'categorias'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    cuenta_id = db.Column(db.Integer, db.ForeignKey('cuentas_bancarias.id'), nullable=False)
