from flask import Flask
from utilidades.seguridad import generar_token_csrf
from rutas.cuenta_bancaria_rutas import cuenta_rutas
from rutas.categoria_rutas import categoria_rutas
from rutas.presupuesto_rutas import presupuesto_rutas
from rutas.transaccion_rutas import transaccion_rutas
from rutas.usuario_rutas import usuario_rutas
from rutas.index_rutas import index_rutas
from configuracion.configuracion import crear_app
from utilidades.logging import init_logging

def create_app():
    app = crear_app()
    app.register_blueprint(cuenta_rutas, url_prefix='/cuentas')
    app.register_blueprint(categoria_rutas, url_prefix='/api')
    app.register_blueprint(presupuesto_rutas, url_prefix='/api')
    app.register_blueprint(transaccion_rutas, url_prefix='/transacciones')
    app.register_blueprint(usuario_rutas, url_prefix='/api')
    app.register_blueprint(index_rutas)

    init_logging(app)

    @app.context_processor
    def inject_csrf_token():
        return dict(csrf_token=generar_token_csrf)


    return app

if __name__ == '__main__':
    app = create_app()
    (app.run(debug=True))
        
