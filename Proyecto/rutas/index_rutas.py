from flask import Blueprint, render_template, session
from flask import redirect, url_for, request, flash
from servicios.usuario_servicio import UsuarioServicio

index_rutas = Blueprint('index_rutas', __name__, template_folder='../templates')

@index_rutas.route('/')
def home():
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return redirect(url_for('usuario_rutas.login'))

    usuario = UsuarioServicio.datos_usuario(usuario_id)
    resumen = UsuarioServicio.obtener_resumen(usuario_id)

    return render_template(
        'index.html',
        usuario=usuario,
        **resumen
    )
