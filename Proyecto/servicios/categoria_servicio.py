import logging
from modelos.categoria import Categoria
from servicios.base_datos import ServicioBaseDatos

class CategoriaServicio:
    
    @staticmethod
    def crear_categoria(nombre, cuenta_id):
        nueva_categoria = Categoria(nombre=nombre, cuenta_id=cuenta_id)
        try:
            ServicioBaseDatos.agregar(nueva_categoria)
            logging.info("Categoría creada: %s para cuenta %s", nombre, cuenta_id)
        except Exception as e:
            logging.error("Error al crear categoría (%s) para cuenta %s: %s", nombre, cuenta_id, e)
            raise e
        return nueva_categoria

    @staticmethod
    def obtener_categorias(cuenta_id):
        categorias = ServicioBaseDatos.obtener_con_filtro(Categoria, [Categoria.cuenta_id == cuenta_id])
        logging.info("Obtenidas %d categorías para la cuenta %s", len(categorias), cuenta_id)
        return categorias
    
    @staticmethod
    def actualizar_categoria(categoria_id, nombre):
        categoria = ServicioBaseDatos.obtener_por_id(Categoria, categoria_id)
        if categoria:
            old_name = categoria.nombre
            categoria.nombre = nombre
            try:
                ServicioBaseDatos.actualizar()
                logging.info("Categoría actualizada: ID %s, de '%s' a '%s'", categoria_id, old_name, nombre)
            except Exception as e:
                logging.error("Error al actualizar categoría ID %s: %s", categoria_id, e)
                raise e
        else:
            logging.warning("Categoría no encontrada para actualizar: ID %s", categoria_id)
        return categoria

    @staticmethod
    def eliminar_categoria(categoria_id):
        categoria = ServicioBaseDatos.obtener_por_id(Categoria, categoria_id)
        if categoria:
            try:
                ServicioBaseDatos.eliminar(categoria)
                logging.info("Categoría eliminada: ID %s", categoria_id)
                return True
            except Exception as e:
                logging.error("Error al eliminar categoría ID %s: %s", categoria_id, e)
                raise e
        else:
            logging.warning("Intento de eliminar categoría inexistente: ID %s", categoria_id)
        return False

    @staticmethod
    def obtener_categorias_por_usuario(usuario_id):
        from modelos.cuenta_bancaria import CuentaBancaria
        cuentas = ServicioBaseDatos.obtener_con_filtro(CuentaBancaria, [CuentaBancaria.usuario_id == usuario_id])
        categorias = []
        for cuenta in cuentas:
            categorias_cuenta = ServicioBaseDatos.obtener_con_filtro(Categoria, [Categoria.cuenta_id == cuenta.id])
            categorias.extend(categorias_cuenta)
        logging.info("Obtenidas %d categorías para el usuario %s", len(categorias), usuario_id)
        return categorias
