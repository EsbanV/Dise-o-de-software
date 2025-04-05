from configuracion.extensiones import db

class Presupuesto(db.Model):
    __tablename__ = 'presupuestos'
    id = db.Column(db.Integer, primary_key=True)
    monto_asignado = db.Column(db.Float, nullable=False)
    monto_gastado = db.Column(db.Float, default=0)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
