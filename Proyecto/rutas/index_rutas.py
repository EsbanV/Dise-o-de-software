from flask import Blueprint, render_template, session
from flask import redirect, url_for, request, current_app
from modelos import CuentaBancaria

index_rutas = Blueprint('index_rutas', __name__, template_folder='../templates')

@index_rutas.route('/')
def home():
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return redirect(url_for('usuario_rutas.login'))

    cuenta_id = request.args.get('cuenta_id', type=int)

    try:
        usuario = current_app.usuario_facade.datos_usuario(usuario_id)
    except ValueError:
        session.pop('usuario_id', None)
        return redirect(url_for('usuario_rutas.login'))
    
    notificaciones = current_app.comunidad_facade.obtener_notificaciones(usuario_id)


    if not cuenta_id:
        cuenta = current_app.cuenta_bancaria_facade.obtener_primer_cuenta(usuario_id)
        cuenta_id = cuenta.id if cuenta else None

    if cuenta_id:
        resumen = current_app.usuario_facade.obtener_resumen(usuario_id, cuenta_id)
        datos_grafico = current_app.grafico_facade.obtener_datos_crudos(cuenta_id)
        grafico_gastos_categoria = current_app.grafico_facade.obtener_datos_categorias_gasto(cuenta_id)
    else:
        resumen = {'cuentas': [], 'cuenta': None, 'categorias': [], 'total_ingresos': 0, 'total_gastos': 0}
        datos_grafico = {'ingresos': 0, 'gastos': 0, 'balance_neto': 0}
        grafico_gastos_categoria = []

    return render_template(
        'index.html',
        usuario=usuario,
        datos_grafico=datos_grafico,
        datos_grafico_categoria=grafico_gastos_categoria,
        **resumen,
        notificaciones=notificaciones
    )
