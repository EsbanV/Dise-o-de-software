from flask.views import MethodView
from flask import render_template, request, redirect, url_for, flash, session
from cuenta_bancaria.controlador import (
    obtener_cuentas_bancarias_controlador,
    crear_cuenta_bancaria_controlador,
    actualizar_cuenta_controlador,
    eliminar_cuenta_bancaria_controlador
)

class VistaCuentas(MethodView):
    def get(self):
        return obtener_cuentas_bancarias_controlador()
    def post(self):
        crear_cuenta_bancaria_controlador()
        return redirect(url_for('cuenta_rutas.vista_cuentas'))

class VistaCuentaDetalle(MethodView):
    def get(self, cuenta_id):
        return actualizar_cuenta_controlador(cuenta_id)
    def post(self, cuenta_id):
        actualizar_cuenta_controlador(cuenta_id)
        return redirect(url_for('cuenta_rutas.vista_cuentas'))

class VistaCuentaEliminar(MethodView):
    def post(self, cuenta_id):
        return eliminar_cuenta_bancaria_controlador(cuenta_id)
