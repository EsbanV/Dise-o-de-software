# rutas/usuario_rutas.py
from flask import Blueprint
from controladores.usuario_controlador import (registrar_usuario_controller, login_controller, logout_controller)

usuario_rutas = Blueprint('usuario_rutas', __name__, template_folder='../templates')

@usuario_rutas.route('/registro', methods=['GET', 'POST'])
def registrar_usuario():
    return registrar_usuario_controller()

@usuario_rutas.route('/login', methods=['GET', 'POST'])
def login():
    return login_controller()

@usuario_rutas.route('/logout')
def logout():
    return logout_controller()
