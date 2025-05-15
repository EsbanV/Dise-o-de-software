from flask import Blueprint, render_template, session
from flask import redirect, url_for, request, flash
from servicios.usuario_servicio import UsuarioServicio
from servicios.grafico_servicio import GraficoServicio
from modelos.cuenta_bancaria import CuentaBancaria
from servicios.base_datos import ServicioBaseDatos
from servicios.notificacion_servicio import NotificacionService

index_rutas = Blueprint('index_rutas', __name__, template_folder='../templates')

@index_rutas.route('/')
def home():
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return redirect(url_for('usuario_rutas.login'))

    cuenta_id = request.args.get('cuenta_id', type=int)

    try:
        usuario = UsuarioServicio.datos_usuario(usuario_id)
    except ValueError:
        session.pop('usuario_id', None)
        return redirect(url_for('usuario_rutas.login'))
    
    notificaciones = NotificacionService.obtener_notificaciones(usuario_id)


    if not cuenta_id:
        cuenta = ServicioBaseDatos.obtener_unico_con_filtro(
            CuentaBancaria, 
            [CuentaBancaria.usuario_id == usuario_id]
        )
        if cuenta:
            cuenta_id = cuenta.id
        else:
            cuenta_id = None

    if cuenta_id:
        resumen = UsuarioServicio.obtener_resumen(usuario_id, cuenta_id)
        datos_grafico = GraficoServicio.obtener_datos_crudos(cuenta_id)
        grafico_gastos_categoria = GraficoServicio.obtener_datos_categorias_gasto(cuenta_id)
    else:
        resumen = {'cuentas': [], 'cuenta': None, 'categorias': [], 'total_ingresos': 0, 'total_gastos': 0}
        datos_grafico = {'ingresos': 0, 'gastos': 0, 'balance_neto': 0}
        grafico_gastos_categoria = []

    return render_template(
        'index.html',
        usuario=usuario,
        datos_grafico=datos_grafico,
        datos_grafico_categoria=grafico_gastos_categoria,
        **resumen
    )
