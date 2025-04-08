import logging
from modelos.categoria import Categoria
from servicios.base_datos import ServicioBaseDatos

class CategoriaServicio:
    
    @staticmethod
    def crear_categoria(nombre, cuenta_id):
        nueva_categoria = Categoria(nombre=nombre, cuenta_id=cuenta_id)
        try:
            ServicioBaseDatos.agregar(nueva_categoria)
        except Exception as e:
            logging.error("Error al crear categoría: %s", e)
            raise e
        return nueva_categoria

    @staticmethod
    def obtener_categorias(cuenta_id):
        return Categoria.query.filter_by(cuenta_id=cuenta_id).all()
