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
    usuario = UsuarioServicio.obtener_usuario_por_id(usuario_id)
    cuentas_bancarias = CuentaBancariaServicio.obtener_cuentas(usuario_id)
    categorias = CategoriaServicio.obtener_categorias(usuario_id)
    transacciones = TransaccionServicio.obtener_transacciones(usuario_id)
    presupuestos = PresupuestoServicio.obtener_presupuesto(usuario_id)
    return render_template('index.html', usuario=usuario, cuentas_bancarias=cuentas_bancarias)
