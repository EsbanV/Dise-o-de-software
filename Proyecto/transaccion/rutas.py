from flask import Blueprint
from transaccion.vistas import (
    VistaTransacciones,
    VistaTransaccionDetalle,
    VistaTransaccionEliminar
)

transaccion = Blueprint('transaccion', __name__, template_folder='templates')

transaccion.add_url_rule(
        '/transacciones',
        view_func=VistaTransacciones.as_view('vista_transacciones'),
        methods=['GET', 'POST']
)
transaccion.add_url_rule(
        '/transacciones/actualizar/<int:transaccion_id>',
        view_func=VistaTransaccionDetalle.as_view('detalle_transaccion'),
        methods=['GET', 'POST']
)
transaccion.add_url_rule(
        '/transacciones/eliminar/<int:transaccion_id>',
        view_func=VistaTransaccionEliminar.as_view('eliminar_transaccion'),
        methods=['POST']
)