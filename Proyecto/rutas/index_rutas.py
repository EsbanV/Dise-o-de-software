from flask import Blueprint, render_template, session
from flask import redirect, url_for, request, flash
from servicios.usuario_servicio import UsuarioServicio
from servicios.cuenta_bancaria_servicio import CuentaBancariaServicio
from servicios.transaccion_servicio import TransaccionServicio
from servicios.presupuesto_servicio import PresupuestoServicio
from servicios.categoria_servicio import CategoriaServicio
index_rutas = Blueprint('index_rutas', __name__, template_folder='../templates')

@index_rutas.route('/')
def home():
    usuario_id = session.get('usuario_id') 
    if not usuario_id:
        return render_template('login.html')

    try:
        usuario = UsuarioServicio.datos_usuario(usuario_id)
    except ValueError:
        session.pop('usuario_id', None)
        flash("La sesión ha expirado. Por favor, inicia sesión nuevamente.", "warning")
        return redirect(url_for('usuario_rutas.login'))
    return render_template('index.html', usuario=usuario)
