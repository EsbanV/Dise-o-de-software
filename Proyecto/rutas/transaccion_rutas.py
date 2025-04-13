from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, session
from servicios.transaccion_servicio import TransaccionServicio

transaccion_rutas = Blueprint('transaccion_rutas', __name__)

@transaccion_rutas.route('/transacciones_vista', methods=['GET', 'POST'])
def gestionar_transacciones():
    categoria_id = request.args.get('categoria_id', type=int)
    if not categoria_id:
        flash('Debe seleccionar una categoría para ver las transacciones.', 'warning')
        return redirect(url_for('index_rutas.home'))
    
    if request.method == 'POST':
        monto = request.form.get('monto')
        try:
            monto = float(monto)
            TransaccionServicio.registrar_transaccion(categoria_id, monto)
            flash('Transacción registrada.', 'success')
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
        return redirect(url_for('transaccion_rutas.gestionar_transacciones', categoria_id=categoria_id))
    
    transacciones = TransaccionServicio.obtener_transacciones(categoria_id)
    return render_template('transacciones.html', categoria_id=categoria_id, transacciones=transacciones)

@transaccion_rutas.route('/transacciones/actualizar/<int:transaccion_id>', methods=['GET', 'POST'])
def actualizar_transaccion_vista(transaccion_id):
    from modelos.transaccion import Transaccion
    transaccion = Transaccion.query.get(transaccion_id)
    if not transaccion:
        flash('Transacción no encontrada.', 'danger')
        return redirect(url_for('index_rutas.home'))
    if request.method == 'POST':
        try:
            nuevo_monto = float(request.form.get('monto'))
            TransaccionServicio.actualizar_transaccion(transaccion_id, nuevo_monto)
            flash('Transacción actualizada.', 'success')
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
        return redirect(url_for('transaccion_rutas.gestionar_transacciones', categoria_id=transaccion.categoria_id))
    return render_template('transaccion_actualizar.html', transaccion=transaccion)

@transaccion_rutas.route('/transacciones/eliminar/<int:transaccion_id>', methods=['POST'])
def eliminar_transaccion_vista(transaccion_id):
    transaccion = TransaccionServicio.eliminar_transaccion(transaccion_id)
    if transaccion:
        flash('Transacción eliminada.', 'success')
    else:
        flash('Transacción no encontrada.', 'danger')
    # Redirigimos a la vista de transacciones para la misma categoría
    categoria_id = transaccion.categoria_id if transaccion else 0
    return redirect(url_for('transaccion_rutas.gestionar_transacciones', categoria_id=categoria_id))
