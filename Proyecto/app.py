from flask import Flask
from utilidades.seguridad import generar_token_csrf
from cuenta_bancaria.rutas import cuenta_bancaria as cuenta_rutas
from categoria.rutas import categoria as categoria_rutas
from presupuesto.rutas import presupuesto as presupuesto_rutas
from transaccion.rutas import transaccion as transaccion_rutas
from usuario.rutas import usuario as usuario_rutas
from rutas.index_rutas import index_rutas
from configuracion.configuracion import crear_app
from utilidades.logging import init_logging

def create_app():
    app = crear_app()
    app.register_blueprint(cuenta_rutas, url_prefix='/api')
    app.register_blueprint(categoria_rutas, url_prefix='/api')
    app.register_blueprint(presupuesto_rutas, url_prefix='/api')
    app.register_blueprint(transaccion_rutas, url_prefix='/api')
    app.register_blueprint(usuario_rutas, url_prefix='/api')
    app.register_blueprint(index_rutas)

    init_logging(app)

    @app.context_processor
    def inject_csrf_token():
        return dict(csrf_token=generar_token_csrf)


    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
