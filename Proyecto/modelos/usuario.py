from configuracion.extensiones import db
from sqlalchemy.orm import relationship

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    activo = db.Column(db.Boolean, default=True)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    contrasena = db.Column(db.String(255), nullable=False)
    
    cuentas_bancarias = relationship("CuentaBancaria", back_populates="usuario", passive_deletes=True)

    def __repr__(self):
        return f'<Usuario {self.id} - {self.nombre}>'