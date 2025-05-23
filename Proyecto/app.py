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

from servicios.FinanzasFacade import (UsuarioFacade, CuentaBancariaFacade, CategoriaFacade,
                                      PresupuestoFacade, TransaccionFacade, 
                                      GraficoFacade, ComunidadFacade
                                     )

def create_app():
    app = crear_app()

    repositorio = ServicioBaseDatos()
    
    presupuesto_servicio = PresupuestoServicio(repositorio)
    categoria_servicio = CategoriaServicio(repositorio, presupuesto_servicio)
    cuenta_bancaria_servicio = CuentaBancariaServicio(repositorio, categoria_servicio)
    transaccion_servicio = TransaccionServicio(repositorio)
    usuario_servicio = UsuarioServicio(repositorio, cuenta_bancaria_servicio, categoria_servicio, transaccion_servicio)
    autor_servicio = AutorService(repositorio, usuario_servicio)
    publicacion_servicio = PublicacionService(repositorio, usuario_servicio)
    grafico_servicio = GraficoServicio(repositorio)
    notificacion_servicio = NotificacionService(repositorio)
    
    app.repositorio = repositorio
    app.usuario_facade = UsuarioFacade(usuario_servicio)
    app.cuenta_bancaria_facade = CuentaBancariaFacade(cuenta_bancaria_servicio)
    app.categoria_facade = CategoriaFacade(categoria_servicio)
    app.presupuesto_facade = PresupuestoFacade(presupuesto_servicio)
    app.transaccion_facade = TransaccionFacade(transaccion_servicio)
    app.grafico_facade = GraficoFacade(grafico_servicio)
    app.comunidad_facade = ComunidadFacade(autor_servicio, publicacion_servicio, notificacion_servicio)

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
        
