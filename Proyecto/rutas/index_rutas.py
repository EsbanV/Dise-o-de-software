from flask import Blueprint, render_template, session, redirect, url_for, request, current_app

index_rutas = Blueprint('index_rutas', __name__, template_folder='../templates')

@index_rutas.route('/')
def home():
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return redirect(url_for('usuario_rutas.login'))

    cuenta_id = request.args.get('cuenta_id', type=int)
    year = request.args.get('year', type=int)
    month = request.args.get('month', type=int)
    day = request.args.get('day', type=int)

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

        # Usar None checks, no if year and month..., para evitar errores con 0
        if year is not None and month is not None and day is not None:
            datos_grafico = current_app.grafico_facade.obtener_datos_crudos_por_dia(cuenta_id, year, month, day)
            grafico_gastos_categoria = current_app.grafico_facade.obtener_datos_categorias_gasto_por_dia(cuenta_id, year, month, day)
            grafico_ingresos_categoria = current_app.grafico_facade.obtener_datos_categorias_ingreso_por_dia(cuenta_id, year, month, day)
        elif year is not None and month is not None:
            datos_grafico = current_app.grafico_facade.obtener_datos_crudos_por_mes(cuenta_id, year, month)
            grafico_gastos_categoria = current_app.grafico_facade.obtener_datos_categorias_gasto_por_mes(cuenta_id, year, month)
            grafico_ingresos_categoria = current_app.grafico_facade.obtener_datos_categorias_ingreso_por_mes(cuenta_id, year, month)
        elif year is not None:
            datos_grafico = current_app.grafico_facade.obtener_datos_crudos_por_anio(cuenta_id, year)
            grafico_gastos_categoria = current_app.grafico_facade.obtener_datos_categorias_gasto_por_anio(cuenta_id, year)
            grafico_ingresos_categoria = current_app.grafico_facade.obtener_datos_categorias_ingreso_por_anio(cuenta_id, year)
        else:
            datos_grafico = current_app.grafico_facade.obtener_datos_crudos(cuenta_id)
            grafico_gastos_categoria = current_app.grafico_facade.obtener_datos_categorias_gasto(cuenta_id)
            grafico_ingresos_categoria = current_app.grafico_facade.obtener_datos_categorias_ingreso(cuenta_id)
    else:
        resumen = {'cuentas': [], 'cuenta': None, 'categorias': [], 'total_ingresos': 0, 'total_gastos': 0}
        datos_grafico = {'ingresos': 0, 'gastos': 0, 'balance_neto': 0}
        grafico_gastos_categoria = []
        grafico_ingresos_categoria = []

    return render_template(
        'index.html',
        usuario=usuario,
        datos_grafico=datos_grafico,
        datos_grafico_categoria=grafico_gastos_categoria,
        datos_grafico_categoria_ingreso=grafico_ingresos_categoria,
        **resumen,
        notificaciones=notificaciones
    )
