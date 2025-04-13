from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, session
from servicios.presupuesto_servicio import PresupuestoServicio
from servicios.categoria_servicio import CategoriaServicio

def gestionar_presupuestos_controller():
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        flash('Necesitas iniciar sesión', 'warning')
        return redirect(url_for('usuario_rutas.login'))
    
    from servicios.categoria_servicio import CategoriaServicio
    categorias = CategoriaServicio.obtener_categorias_por_usuario(usuario_id)
    
    if request.method == 'POST':
        for categoria in categorias:
            monto = request.form.get(f'presupuesto_{categoria.id}')
            if monto is not None:
                try:
                    monto = float(monto)
                except ValueError:
                    monto = 0
                PresupuestoServicio.asignar_presupuesto(categoria.id, monto)
        flash('Presupuestos actualizados correctamente.', 'success')
        return redirect(url_for('presupuesto_rutas.gestionar_presupuestos'))
    
    presupuestos = {}
    for categoria in categorias:
        presupuesto = PresupuestoServicio.obtener_presupuesto(categoria.id)
        presupuestos[categoria.id] = presupuesto
    return render_template('presupuestos.html', categorias=categorias, presupuestos=presupuestos)

def eliminar_presupuesto_controller(presupuesto_id):
    PresupuestoServicio.eliminar_presupuesto(presupuesto_id)
    flash('Presupuesto eliminado.', 'success')
    return redirect(url_for('presupuesto_rutas.gestionar_presupuestos'))
