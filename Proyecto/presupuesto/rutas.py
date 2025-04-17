from flask import Blueprint
from presupuesto.vistas import (
    VistaPresupuestos,
    VistaPresupuestoDetalle,
    VistaPresupuestoEliminar
)

presupuesto = Blueprint('presupuesto', __name__)

presupuesto.add_url_rule(
        '/presupuestos',
        view_func=VistaPresupuestos.as_view('vista_presupuestos'),
        methods=['GET', 'POST']
)
presupuesto.add_url_rule(
        '/presupuestos/eliminar/<int:presupuesto_id>',
        view_func=VistaPresupuestoEliminar.as_view('eliminar_presupuesto'),
        methods=['POST']
)