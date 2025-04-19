from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, session
from servicios.transaccion_servicio import TransaccionServicio
from servicios.cuenta_bancaria_servicio import CuentaBancariaServicio
from servicios.categoria_servicio import CategoriaServicio
from modelos.categoria import TipoCategoria 

transaccion_rutas = Blueprint('transaccion_rutas', __name__)

@transaccion_rutas.route('/transacciones', methods=['GET', 'POST'])
def registrar_transaccion():
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        flash('Necesitas iniciar sesión para registrar transacciones.', 'warning')
        return redirect(url_for('usuario_rutas.login'))

    cuentas = CuentaBancariaServicio.obtener_cuentas(usuario_id)

    cuenta_id = request.args.get('cuenta_id', type=int)
    categorias = []

    if cuenta_id:
        categorias = CategoriaServicio.obtener_categorias(cuenta_id)

    if request.method == 'POST':
        cuenta_id = int(request.form.get('cuenta_id'))
        categoria_id = int(request.form.get('categoria_id'))
        descripcion = request.form.get('descripcion')
        monto = float(request.form.get('monto'))

        categoria = CategoriaServicio.obtener_categoria_por_id(categoria_id)

        if categoria.tipo == TipoCategoria.GASTO:
            monto = -abs(monto)
        else:
            monto = abs(monto)

        try:
            TransaccionServicio.registrar_transaccion(cuenta_id, categoria_id, descripcion, monto)
            flash('Transacción registrada correctamente.', 'success')
        except Exception as e:
            flash(f'Error al registrar la transacción: {str(e)}', 'danger')

        return redirect(url_for('transaccion_rutas.registrar_transaccion', cuenta_id=cuenta_id))

    return render_template('transaccion.html', cuentas=cuentas, categorias=categorias, cuenta_id=cuenta_id)
