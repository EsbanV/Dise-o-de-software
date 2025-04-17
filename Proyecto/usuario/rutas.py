from flask import Blueprint
from usuario.vistas import (
    VistaRegistrarUsuario,
    VistaLogin,
    VistaLogout
)

usuario = Blueprint('usuario', __name__, template_folder='templates')

usuario.add_url_rule(
        '/registro',
        view_func=VistaRegistrarUsuario.as_view('registrar_usuario'),
        methods=['GET', 'POST']
)
usuario.add_url_rule(
        '/login',
        view_func=VistaLogin.as_view('login'),
        methods=['GET', 'POST']
)
usuario.add_url_rule(
        '/logout',
        view_func=VistaLogout.as_view('logout'),
        methods=['GET']
)