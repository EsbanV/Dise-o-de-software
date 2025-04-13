from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, session
from servicios.presupuesto_servicio import PresupuestoServicio
from servicios.categoria_servicio import CategoriaServicio

presupuesto_rutas = Blueprint('presupuesto_rutas', __name__)

@presupuesto_rutas.route('/asignar_presupuestos', methods=['POST'])
def asignar_presupuestos():
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        flash('Necesitas iniciar sesión', 'warning')
        return redirect(url_for('usuario_rutas.login'))
    
    categorias = CategoriaServicio.obtener_categorias_por_usuario(usuario_id)
    for categoria in categorias:
        monto = request.form.get(f'presupuesto_{categoria.id}')
        if monto is not None:
            try:
                monto = float(monto)
            except ValueError:
                monto = 0
            PresupuestoServicio.asignar_presupuesto(categoria.id, monto)
    
    flash('Presupuestos actualizados correctamente.', 'success')
    return redirect(url_for('presupuesto_rutas.ver_presupuestos'))


@presupuesto_rutas.route('/presupuestos/<int:categoria_id>', methods=['GET'])
def obtener_presupuesto(categoria_id):
    presupuesto = PresupuestoServicio.obtener_presupuesto(categoria_id)
    if presupuesto:
        return jsonify({
            "id": presupuesto.id,
            "categoria_id": presupuesto.categoria_id,
            "monto_asignado": presupuesto.monto_asignado,
            "monto_gastado": presupuesto.monto_gastado
        }), 200
    else:
        return jsonify({"mensaje": "Presupuesto no encontrado"}), 404


@presupuesto_rutas.route('/presupuestos', methods=['GET'])
def ver_presupuestos():
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        flash('Necesitas iniciar sesión', 'warning')
        return redirect(url_for('usuario_rutas.login'))
    
    categorias = CategoriaServicio.obtener_categorias_por_usuario(usuario_id)
    presupuestos_data = {}
    
    for categoria in categorias:
        presupuesto = PresupuestoServicio.obtener_presupuesto(categoria.id)
        if presupuesto:
            presupuestos_data[categoria.id] = {
                'monto_asignado': presupuesto.monto_asignado,
                'monto_gastado': presupuesto.monto_gastado
            }
        else:
            presupuestos_data[categoria.id] = {
                'monto_asignado': 0,
                'monto_gastado': 0
            }
    
    return render_template('presupuestos.html', 
                         categorias=categorias, 
                         presupuestos=presupuestos_data)
