from flask.views import MethodView
from flask import render_template, request, redirect, url_for, flash, session

from transaccion.controlador import (
    obtener_transacciones_controlador,
    crear_transaccion_controlador,
    actualizar_transaccion_controlador,
    eliminar_transaccion_controlador
)

class VistaTransacciones(MethodView):
    def get(self):
        return obtener_transacciones_controlador()
    def post(self):
        crear_transaccion_controlador()
        return redirect(url_for('transaccion_rutas.vista_transacciones'))

class VistaTransaccionDetalle(MethodView):
    def get(self, transaccion_id):
        return actualizar_transaccion_controlador(transaccion_id)
    def post(self, transaccion_id):
        actualizar_transaccion_controlador(transaccion_id)
        return redirect(url_for('transaccion_rutas.vista_transacciones'))

class VistaTransaccionEliminar(MethodView):
    def post(self, transaccion_id):
        return eliminar_transaccion_controlador(transaccion_id)
