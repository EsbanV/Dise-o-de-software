from flask import Blueprint, request, render_template, redirect, url_for, flash, session, current_app
transaccion_rutas = Blueprint('transaccion_rutas', __name__)

@transaccion_rutas.route('/transacciones', methods=['GET', 'POST'])
def registrar_transaccion():
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        flash('Necesitas iniciar sesión para registrar transacciones.', 'warning')
        return redirect(url_for('usuario_rutas.login'))

    cuentas = current_app.cuenta_bancaria_facade.obtener_cuentas(usuario_id)
    cuenta_id = request.args.get('cuenta_id', type=int)
    categorias = current_app.categoria_facade.obtener_categorias(cuenta_id) if cuenta_id else []

    if request.method == 'POST':
        cuenta_id = request.form.get('cuenta_id')
        categoria_id = request.form.get('categoria_id')
        descripcion = request.form.get('descripcion')
        monto = request.form.get('monto')

        try:
            current_app.transaccion_facade.registrar_transaccion(cuenta_id, categoria_id, descripcion, monto)
            flash('Transacción registrada correctamente.', 'success')
        except Exception as e:
            flash(f'Error al registrar la transacción: {str(e)}', 'danger')

        return redirect(url_for('transaccion_rutas.registrar_transaccion', cuenta_id=cuenta_id))

    return render_template('transaccion.html', cuentas=cuentas, categorias=categorias, cuenta_id=cuenta_id)
