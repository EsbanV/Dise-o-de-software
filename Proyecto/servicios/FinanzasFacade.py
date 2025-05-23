
class UsuarioFacade:
    def __init__(self, usuario_servicio):
        self.usuario_servicio = usuario_servicio

    def registrar_usuario(self, nombre, correo, contrasena):
        return self.usuario_servicio.registrar_usuario(nombre, correo, contrasena)

    def iniciar_sesion(self, correo, contrasena):
        return self.usuario_servicio.iniciar_sesion(correo, contrasena)

    def actualizar_perfil(self, usuario_id, nombre=None, correo=None, contrasena=None):
        return self.usuario_servicio.actualizar_usuario(usuario_id, nombre, correo, contrasena)

    def eliminar_usuario(self, usuario_id):
        return self.usuario_servicio.eliminar_usuario(usuario_id)
    
    def obtener_usuario_activo(self, usuario_id):
        return self.usuario_servicio.obtener_usuario_activo(usuario_id)
    
    def obtener_resumen(self, usuario_id, cuenta_id=None):
        return self.usuario_servicio.obtener_resumen(usuario_id, cuenta_id)
    
    def datos_usuario(self, usuario_id):
        return self.usuario_servicio.datos_usuario(usuario_id)

class CuentaBancariaFacade:
    def __init__(self, cuenta_bancaria_servicio):
        self.cuenta_bancaria_servicio = cuenta_bancaria_servicio

    def crear_cuenta(self, nombre, saldo_inicial, usuario_id):
        return self.cuenta_bancaria_servicio.crear_cuenta(nombre, saldo_inicial, usuario_id)

    def obtener_cuentas(self, usuario_id):
        return self.cuenta_bancaria_servicio.obtener_cuentas(usuario_id)
    
    def obtener_cuenta_por_id(self, cuenta_id):
        return self.cuenta_bancaria_servicio.obtener_cuenta_por_id(cuenta_id)
    
    def obtener_primer_cuenta(self, usuario_id):
        return self.cuenta_bancaria_servicio.obtener_primer_cuenta(usuario_id)

    def actualizar_cuenta(self, cuenta_id, nombre=None, saldo=None):
        return self.cuenta_bancaria_servicio.actualizar_cuenta(cuenta_id, nombre, saldo)

    def eliminar_cuenta(self, cuenta_id):
        return self.cuenta_bancaria_servicio.eliminar_cuenta(cuenta_id)

class CategoriaFacade:
    def __init__(self, categoria_servicio):
        self.categoria_servicio = categoria_servicio

    def crear_categoria(self, cuenta_id, nombre, tipo, presupuesto=None):
        return self.categoria_servicio.crear_categoria(cuenta_id, nombre, tipo, presupuesto)

    def obtener_categorias(self, cuenta_id):
        return self.categoria_servicio.obtener_categorias(cuenta_id)
    
    def obtener_categorias_por_usuario(self, usuario_id):
        return self.categoria_servicio.obtener_categorias_por_usuario(usuario_id)
    
    def obtener_categoria_por_id(self, categoria_id):
        return self.categoria_servicio.obtener_categoria_por_id(categoria_id)
    
    def obtener_categorias_filtradas(self, cuenta_id, tipo=None):
        return self.categoria_servicio.obtener_categorias_filtradas(cuenta_id, tipo)

    def actualizar_categoria(self, categoria_id, nombre):
        return self.categoria_servicio.actualizar_categoria(categoria_id, nombre)

    def eliminar_categoria(self, categoria_id):
        return self.categoria_servicio.eliminar_categoria(categoria_id)

class PresupuestoFacade:
    def __init__(self, presupuesto_servicio):
        self.presupuesto_servicio = presupuesto_servicio

    def asignar_presupuesto(self, categoria_id, monto):
        return self.presupuesto_servicio.asignar_presupuesto(categoria_id, monto)

    def obtener_presupuesto(self, categoria_id):
        return self.presupuesto_servicio.obtener_presupuesto(categoria_id)

    def eliminar_presupuesto(self, presupuesto_id):
        return self.presupuesto_servicio.eliminar_presupuesto(presupuesto_id)

class TransaccionFacade:
    def __init__(self, transaccion_servicio):
        self.transaccion_servicio = transaccion_servicio

    def registrar_transaccion(self, cuenta_id, categoria_id, descripcion, monto):
        return self.transaccion_servicio.registrar_transaccion(cuenta_id, categoria_id, descripcion, monto)

    def obtener_transacciones_por_cuenta(self, cuenta_id):
        return self.transaccion_servicio.obtener_transacciones_por_cuenta(cuenta_id)

    def obtener_transacciones_por_categoria(self, categoria_id):
        return self.transaccion_servicio.obtener_transacciones_por_categoria(categoria_id)
    
    def obtener_transacciones_por_categoria_y_cuenta(self, cuenta_id, categoria_id):
        return self.transaccion_servicio.obtener_transacciones_por_categoria_y_cuenta(cuenta_id, categoria_id)

    def actualizar_transaccion(self, transaccion_id, nuevo_monto):
        return self.transaccion_servicio.actualizar_transaccion(transaccion_id, nuevo_monto)

    def eliminar_transaccion(self, transaccion_id):
        return self.transaccion_servicio.eliminar_transaccion(transaccion_id)

class GraficoFacade:
    def __init__(self, grafico_servicio):
        self.grafico_servicio = grafico_servicio

    def obtener_datos_crudos(self, cuenta_id):
        return self.grafico_servicio.obtener_datos_crudos(cuenta_id)

    def obtener_datos_categorias_gasto(self, cuenta_id):
        return self.grafico_servicio.obtener_datos_categorias_gasto(cuenta_id)

class ComunidadFacade:
    def __init__(self, autor_servicio, publicacion_servicio, notificacion_servicio):
        self.autor_servicio = autor_servicio
        self.publicacion_servicio = publicacion_servicio
        self.notificacion_servicio = notificacion_servicio

    # Autores
    def suscribirse_autor(self, subscriber_id, autor_id):
        return self.autor_servicio.suscribirse_autor(subscriber_id, autor_id)

    def desuscribirse_autor(self, subscriber_id, autor_id):
        return self.autor_servicio.desuscribirse_autor(subscriber_id, autor_id)

    # Publicaciones y comentarios
    def crear_publicacion(self, usuario_id, titulo, contenido):
        return self.publicacion_servicio.crear_publicacion(usuario_id, titulo, contenido)
    
    def obtener_publicacion(self, publicacion_id: int):
        return self.publicacion_servicio.obtener_publicacion_o_404(publicacion_id)

    def obtener_publicaciones(self):
        return self.publicacion_servicio.obtener_publicaciones()

    def agregar_comentario(self, publicacion_id, usuario_id, contenido):
        return self.publicacion_servicio.agregar_comentario(publicacion_id, usuario_id, contenido)

    # Notificaciones
    def obtener_notificaciones(self, usuario_id):
        return self.notificacion_servicio.obtener_notificaciones(usuario_id)

    def marcar_notificacion_leida(self, notificacion_id):
        return self.notificacion_servicio.marcar_notificacion_leida(notificacion_id)
