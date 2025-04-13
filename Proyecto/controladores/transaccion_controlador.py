# controladores/transaccion_controlador.py
from flask import request, render_template, redirect, url_for, flash, session
from servicios.transaccion_servicio import TransaccionServicio
from modelos.transaccion import Transaccion

def gestionar_transacciones_controller():
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

def actualizar_transaccion_controller(transaccion_id):
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

def eliminar_transaccion_controller(transaccion_id):
    transaccion = TransaccionServicio.eliminar_transaccion(transaccion_id)
    if transaccion:
        flash('Transacción eliminada.', 'success')
    else:
        flash('Transacción no encontrada.', 'danger')
    categoria_id = transaccion.categoria_id if transaccion else 0
    return redirect(url_for('transaccion_rutas.gestionar_transacciones', categoria_id=categoria_id))
