import logging
from categoria.modelo import Categoria
from categoria.repositorio import CategoriaRepositorio
from cuenta_bancaria.repositorio import CuentaBancariaRepositorio

class CategoriaServicio:
    _repositorio = CategoriaRepositorio()

    @staticmethod
    def crear_categoria(nombre, cuenta_id):
        if not nombre:
            logging.error("El nombre de la categoría es requerido")
            raise ValueError("El nombre de la categoría es requerido")
        try:
            nueva_categoria = Categoria(nombre=nombre, cuenta_id=cuenta_id)
            categoria = CategoriaServicio._repositorio.crear(nueva_categoria)
            logging.info("Categoría creada: %s para cuenta %s", nombre, cuenta_id)
            return categoria
        except Exception as e:
            logging.error("Error al crear categoría (%s) para cuenta %s: %s", nombre, cuenta_id, e)
            raise e

    @staticmethod
    def obtener_categorias(cuenta_id):
        try:
            categorias = CategoriaServicio._repositorio.obtener_por_cuenta(cuenta_id)
            logging.info("Obtenidas %d categorías para la cuenta %s", len(categorias), cuenta_id)
            return categorias
        except Exception as e:
            logging.error("Error al obtener categorías para cuenta %s: %s", cuenta_id, e)
            raise e

    @staticmethod
    def actualizar_categoria(categoria_id, nombre):
        categoria = CategoriaServicio._repositorio.obtener_por_id(categoria_id)
        if categoria:
            old_name = categoria.nombre
            categoria.nombre = nombre
            try:
                CategoriaServicio._repositorio.actualizar(categoria)
                logging.info("Categoría actualizada: ID %s, de '%s' a '%s'", categoria_id, old_name, nombre)
                return categoria
            except Exception as e:
                logging.error("Error al actualizar categoría ID %s: %s", categoria_id, e)
                raise e
        else:
            logging.warning("Categoría no encontrada para actualizar: ID %s", categoria_id)
        return None

    @staticmethod
    def eliminar_categoria(categoria_id):
        try:
            resultado = CategoriaServicio._repositorio.eliminar(categoria_id)
            if resultado:
                logging.info("Categoría eliminada: ID %s", categoria_id)
            else:
                logging.warning("Intento de eliminar categoría inexistente: ID %s", categoria_id)
            return resultado
        except Exception as e:
            logging.error("Error al eliminar categoría ID %s: %s", categoria_id, e)
            raise e

    @staticmethod
    def obtener_categorias_por_usuario(usuario_id):
        cuenta_repo = CuentaBancariaRepositorio()
        cuentas = cuenta_repo.obtener_por_usuario(usuario_id)
        categorias = []
        for cuenta in cuentas:
            categorias_cuenta = CategoriaServicio.obtener_categorias(cuenta.id)
            categorias.extend(categorias_cuenta)
        logging.info("Obtenidas %d categorías para el usuario %s", len(categorias), usuario_id)
        return categorias
