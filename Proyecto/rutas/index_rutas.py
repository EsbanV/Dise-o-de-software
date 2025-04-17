from flask import Blueprint, render_template, session
from flask import redirect, url_for, request, flash
from usuario.servicio import UsuarioServicio
from cuenta_bancaria.servicio import CuentaBancariaServicio
from transaccion.servicio import TransaccionServicio
from presupuesto.servicio import PresupuestoServicio
from categoria.servicio import CategoriaServicio
index_rutas = Blueprint('index_rutas', __name__, template_folder='../templates')

@index_rutas.route('/')
def home():
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return render_template('login.html')
    
    usuario = UsuarioServicio.ingresar_usuario(usuario_id)
    cuentas_bancarias = CuentaBancariaServicio.obtener_cuentas_bancarias(usuario_id)
    
    selected_cuenta_id = request.args.get('cuenta_id', type=int)
    if not selected_cuenta_id and cuentas_bancarias:
        selected_cuenta_id = cuentas_bancarias[0].id

    categorias = CategoriaServicio.obtener_categorias(selected_cuenta_id) if selected_cuenta_id else []
    
    chart_categorias_labels = [categoria.nombre for categoria in categorias]
    chart_categorias_values = []
    for categoria in categorias:
        presupuesto = PresupuestoServicio.obtener_presupuesto(categoria.id)
        monto = presupuesto.monto_asignado if presupuesto else 0
        chart_categorias_values.append(monto)
    
    chart_dissection_labels = ["Enero", "Febrero", "Marzo"]
    chart_dissection_values = [100, 200, 150]
    
    chart_ingresos_gastos_labels = ["Enero", "Febrero", "Marzo"]
    chart_ingresos = []
    chart_gastos = []
    for categoria in categorias:
        transacciones = TransaccionServicio.obtener_transacciones(categoria.id)

        for t in transacciones:
            if t.monto > 0:
                chart_ingresos.append(t.monto)
            else:
                chart_gastos.append(t.monto)
    

    transacciones = []
    for categoria in categorias:
        transacciones.extend(TransaccionServicio.obtener_transacciones(categoria.id))
    
    total_ingresos = sum(ingresos for ingresos in chart_ingresos)
    total_gastos = sum(gastos for gastos in chart_gastos)
    
    active_account = None
    for cuenta in cuentas_bancarias:
        if cuenta.id == selected_cuenta_id:
            active_account = cuenta
            break
    
    return render_template(
        'index.html',
        usuario=usuario,
        cuentas_bancarias=cuentas_bancarias,
        selected_cuenta_id=selected_cuenta_id,
        categorias=categorias,
        transacciones=transacciones,
        total_ingresos=total_ingresos,
        total_gastos=total_gastos,
        active_account=active_account,
        chart_categorias_labels=chart_categorias_labels,
        chart_categorias_values=chart_categorias_values,
        chart_dissection_labels=chart_dissection_labels,
        chart_dissection_values=chart_dissection_values,
        chart_ingresos_gastos_labels=chart_ingresos_gastos_labels,
        chart_ingresos=chart_ingresos,
        chart_gastos=chart_gastos
    )
