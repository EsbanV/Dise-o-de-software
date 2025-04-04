from flask import Flask
from rutas.cuenta_bancaria_rutas import cuenta_rutas
from rutas.categoria_rutas import categoria_rutas
from rutas.presupuesto_rutas import presupuesto_rutas
from rutas.transaccion_rutas import transaccion_rutas
from rutas.usuario_rutas import usuario_rutas
from rutas.index_rutas import index_rutas

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('configuracion/configuracion.py')
    

    app.register_blueprint(cuenta_rutas, url_prefix='/api')
    app.register_blueprint(categoria_rutas, url_prefix='/api')
    app.register_blueprint(presupuesto_rutas, url_prefix='/api')
    app.register_blueprint(transaccion_rutas, url_prefix='/api')
    app.register_blueprint(usuario_rutas, url_prefix='/api')
    app.register_blueprint(index_rutas)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
