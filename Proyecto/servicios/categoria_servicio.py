import logging
from modelos.categoria import Categoria
from modelos.presupuesto import Presupuesto
from servicios.base_datos import ServicioBaseDatos
from servicios.presupuesto_servicio import PresupuestoServicio
from utilidades.validaciones import validar_nombre

class CategoriaServicio:

    @staticmethod
    def crear_categoria(nombre, tipo, presupuesto, cuenta_id):
        if not validar_nombre(nombre):
            raise ValueError("Nombre de categoría inválido")  

        if tipo == "INGRESO":
            if presupuesto:
                raise ValueError("No puedes asignar presupuesto a una categoria tipo ingreso")

        nueva_categoria = Categoria(nombre=nombre, tipo=tipo, cuenta_id=cuenta_id)
        try:
            ServicioBaseDatos.agregar(nueva_categoria)
            logging.info("Categoría creada: %s para cuenta %s", nombre, tipo, cuenta_id)
        except Exception as e:
            logging.error("Error al crear categoría (%s) para cuenta %s: %s", nombre, tipo, cuenta_id, e)
            raise e
        
        if presupuesto:
            PresupuestoServicio.asignar_presupuesto(nueva_categoria.id, presupuesto)
        return nueva_categoria

    @staticmethod
    def obtener_categorias(cuenta_id):
        categorias = ServicioBaseDatos.obtener_con_filtro(Categoria, [Categoria.cuenta_id == cuenta_id])
        if categorias:
            logging.info("Obtenidas %d categorías para la cuenta %s", len(categorias), cuenta_id)
        else:
            return []
        return categorias

    @staticmethod
    def actualizar_categoria(categoria_id, nombre):
        if not validar_nombre(nombre):
            raise ValueError("Nombre de categoría inválido")

        categoria = ServicioBaseDatos.obtener_por_id(Categoria, categoria_id)
        if not categoria:
            logging.warning("Categoría no encontrada para actualizar: ID %s", categoria_id)
            return None

        old_name = categoria.nombre
        categoria.nombre = nombre
        try:
            ServicioBaseDatos.actualizar()
            logging.info("Categoría actualizada: ID %s, de '%s' a '%s'", categoria_id, old_name, nombre)
        except Exception as e:
            logging.error("Error al actualizar categoría ID %s: %s", categoria_id, e)
            raise e
        return categoria

    @staticmethod
    def eliminar_categoria(categoria_id):
        categoria = ServicioBaseDatos.obtener_por_id(Categoria, categoria_id)
        if not categoria:
            logging.warning("Intento de eliminar categoría inexistente: ID %s", categoria_id)
            return False
        print("tengo algo")

        try:
            print("ostia me elimino")
            ServicioBaseDatos.eliminar(categoria)
            logging.info("Categoría eliminada: ID %s", categoria_id)
            return True
        except Exception as e:
            logging.error("Error al eliminar categoría ID %s: %s", categoria_id, e)
            raise e

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

    @staticmethod
    def obtener_categoria_por_id(categoria_id):
        categoria = ServicioBaseDatos.obtener_por_id(Categoria, categoria_id)
        if categoria:
            logging.info("Categoría encontrada: ID %s, Nombre %s", categoria_id, categoria.nombre)
        else:
            logging.warning("Categoría no encontrada: ID %s", categoria_id)
        return categoria

    @staticmethod
    def obtener_categorias_filtradas(cuenta_id, tipo=None):
        filtros = [Categoria.cuenta_id == cuenta_id]
        if tipo:
            filtros.append(Categoria.tipo == tipo)
        categorias = ServicioBaseDatos.obtener_con_filtro(Categoria, filtros)
        logging.info("Obtenidas %d categorías filtradas para la cuenta %s", len(categorias), cuenta_id)
        return categorias
