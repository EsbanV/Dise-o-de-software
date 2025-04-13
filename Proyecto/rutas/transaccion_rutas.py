from flask import Blueprint
from controladores.transaccion_controlador import (gestionar_transacciones_controller, actualizar_transaccion_controller, eliminar_transaccion_controller)

transaccion_rutas = Blueprint('transaccion_rutas', __name__)

@transaccion_rutas.route('/transacciones_vista', methods=['GET', 'POST'])
def gestionar_transacciones():
    return gestionar_transacciones_controller()

@transaccion_rutas.route('/transacciones/actualizar/<int:transaccion_id>', methods=['GET', 'POST'])
def actualizar_transaccion_vista(transaccion_id):
    return actualizar_transaccion_controller(transaccion_id)

@transaccion_rutas.route('/transacciones/eliminar/<int:transaccion_id>', methods=['POST'])
def eliminar_transaccion_vista(transaccion_id):
    return eliminar_transaccion_controller(transaccion_id)
