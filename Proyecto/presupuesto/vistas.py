from flask.views import MethodView
from flask import render_template, request, redirect, url_for, flash, session

from presupuesto.controlador import (
    controlador_obtener_presupuestos,
    controlador_crear_presupuesto,
    controlador_eliminar_presupuesto
)

class VistaPresupuestos(MethodView):
    def get(self):
        return controlador_obtener_presupuestos()
    def post(self):
        controlador_crear_presupuesto()
        return redirect(url_for('presupuesto_rutas.vista_presupuestos'))

class VistaPresupuestoEliminar(MethodView):
    def post(self, presupuesto_id):
        return controlador_eliminar_presupuesto(presupuesto_id)
