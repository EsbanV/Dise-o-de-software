from flask import Blueprint
from cuenta_bancaria.vistas import (
    VistaCuentas,
    VistaCuentaDetalle,
    VistaCuentaEliminar
)

cuenta_bancaria = Blueprint('cuenta_bancaria', __name__)

cuenta_bancaria.add_url_rule(
        '/cuentas',
        view_func=VistaCuentas.as_view('vista_cuentas'),
        methods=['GET', 'POST']
)
cuenta_bancaria.add_url_rule(
        '/cuentas/actualizar/<int:cuenta_id>',
        view_func=VistaCuentaDetalle.as_view('detalle_cuenta'),
        methods=['GET', 'POST']
)
cuenta_bancaria.add_url_rule(
        '/cuentas/eliminar/<int:cuenta_id>',
        view_func=VistaCuentaEliminar.as_view('eliminar_cuenta'),
        methods=['POST']
)