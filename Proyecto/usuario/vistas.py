from flask.views import MethodView
from flask import render_template, request, redirect, url_for, flash, session

from usuario.controlador import (
    registrar_usuario_controller,
    login_controller,
    logout_controller
)

# USUARIOS (Autenticación)
class VistaRegistrarUsuario(MethodView):
    def get(self):
        return registrar_usuario_controller()
    def post(self):
        registrar_usuario_controller()
        return redirect(url_for('usuario_rutas.login'))

class VistaLogin(MethodView):
    def get(self):
        return login_controller()
    def post(self):
        login_controller()
        return redirect(url_for('usuario_rutas.vista_inicio'))

class VistaLogout(MethodView):
    def get(self):
        return logout_controller()