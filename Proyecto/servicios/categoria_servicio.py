from modelos.categoria import Categoria
from servicios.base_datos import db

class CategoriaServicio:
    @staticmethod
    def crear_categoria(nombre, cuenta_id):
        nueva_categoria = Categoria(nombre=nombre, cuenta_id=cuenta_id)
        db.session.add(nueva_categoria)
        db.session.commit()
        return nueva_categoria

    @staticmethod
    def obtener_categorias(cuenta_id):
        return Categoria.query.filter_by(cuenta_id=cuenta_id).all()
