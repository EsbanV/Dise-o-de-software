import logging
from modelos.categoria import Categoria
from servicios.base_datos import ServicioBaseDatos
from modelos.cuenta_bancaria import CuentaBancaria  # Necesitamos importar CuentaBancaria

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
    
    @staticmethod
    def obtener_categorias_por_usuario(usuario_id):
        # Primero obtenemos todas las cuentas del usuario
        cuentas = CuentaBancaria.query.filter_by(usuario_id=usuario_id).all()
        
        categorias = []
        for cuenta in cuentas:
            # Para cada cuenta, obtenemos sus categorías
            categorias_cuenta = Categoria.query.filter_by(cuenta_id=cuenta.id).all()
            categorias.extend(categorias_cuenta)
        
        return categorias
    
    @staticmethod
    def eliminar_categoria(categoria_id):
        categoria = Categoria.query.get(categoria_id)
        if categoria:
            try:
                ServicioBaseDatos.eliminar(categoria)
                return True
            except Exception as e:
                logging.error("Error al eliminar categoría con ID %s: %s", categoria_id, e)
                raise e
        return False