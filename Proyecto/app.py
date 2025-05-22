from flask import Flask
from utilidades.seguridad import generar_token_csrf
from configuracion.configuracion import crear_app
from utilidades.logging import init_logging

from servicios.base_datos import ServicioBaseDatos
from servicios.usuario_servicio import UsuarioServicio
from servicios.transaccion_servicio import TransaccionServicio
from servicios.categoria_servicio import CategoriaServicio
from servicios.presupuesto_servicio import PresupuestoServicio
from servicios.cuenta_bancaria_servicio import CuentaBancariaServicio
from servicios.autor_servicio import AutorService
from servicios.notificacion_servicio import NotificacionService
from servicios.grafico_servicio import GraficoServicio
from servicios.publicacion_servicio import PublicacionService


def create_app():
    app = crear_app()

    # 1. Instancia el repositorio (una vez)
    repositorio = ServicioBaseDatos()
    
    # 2. Instancia todos los servicios, pasando dependencias necesarias
    presupuesto_servicio = PresupuestoServicio(repositorio)
    categoria_servicio = CategoriaServicio(repositorio, presupuesto_servicio)
    cuenta_bancaria_servicio = CuentaBancariaServicio(repositorio, categoria_servicio)
    transaccion_servicio = TransaccionServicio(repositorio)
    usuario_servicio = UsuarioServicio(repositorio, cuenta_bancaria_servicio, categoria_servicio, transaccion_servicio)
    autor_servicio = AutorService(repositorio, usuario_servicio)
    publicacion_servicio = PublicacionService(repositorio, usuario_servicio)
    grafico_servicio = GraficoServicio(repositorio)
    notificacion_servicio = NotificacionService(repositorio)
    
    # 3. Guarda los servicios en el app context
    app.repositorio = repositorio
    app.presupuesto_servicio = presupuesto_servicio
    app.categoria_servicio = categoria_servicio
    app.cuenta_bancaria_servicio = cuenta_bancaria_servicio
    app.transaccion_servicio = transaccion_servicio
    app.usuario_servicio = usuario_servicio
    app.autor_servicio = autor_servicio
    app.publicacion_servicio = publicacion_servicio
    app.grafico_servicio = grafico_servicio
    app.notificacion_servicio = notificacion_servicio

    # 4. Registra los blueprints (rutas)
    from rutas.cuenta_bancaria_rutas import cuenta_rutas
    from rutas.categoria_rutas import categoria_rutas
    from rutas.presupuesto_rutas import presupuesto_rutas
    from rutas.transaccion_rutas import transaccion_rutas
    from rutas.usuario_rutas import usuario_rutas
    from rutas.index_rutas import index_rutas
    from rutas.api_rutas import api_rutas
    from rutas.autor_rutas import autor_rutas
    from rutas.publicacion_rutas import publicacion_rutas
    from rutas.notificacion_rutas import notificacion_rutas

    app.register_blueprint(cuenta_rutas, url_prefix='/cuentas')
    app.register_blueprint(categoria_rutas, url_prefix='/categorias')
    app.register_blueprint(presupuesto_rutas, url_prefix='/presupuestos')
    app.register_blueprint(usuario_rutas, url_prefix='/usuarios')
    app.register_blueprint(transaccion_rutas, url_prefix='/transacciones')
    app.register_blueprint(api_rutas, url_prefix='/api')
    app.register_blueprint(publicacion_rutas)
    app.register_blueprint(autor_rutas)
    app.register_blueprint(notificacion_rutas)
    app.register_blueprint(index_rutas)

    init_logging(app)

    @app.context_processor
    def inject_csrf_token():
        return dict(csrf_token=generar_token_csrf)


    return app

if __name__ == '__main__':
    app = create_app()
    (app.run(debug=True))
        
