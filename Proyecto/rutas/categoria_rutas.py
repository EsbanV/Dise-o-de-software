from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, session
from servicios.categoria_servicio import CategoriaServicio

categoria_rutas = Blueprint('categoria_rutas', __name__)

@categoria_rutas.route('/categorias_vista', methods=['GET', 'POST'])
def crear_categoria_vista():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        try:
            cuenta_id = int(request.form.get('cuenta_id'))
        except (TypeError, ValueError):
            flash('Debe proporcionar un ID de cuenta válido.', 'warning')
            return redirect(url_for('categoria_rutas.crear_categoria_vista'))
        CategoriaServicio.crear_categoria(nombre, cuenta_id)
        flash('Categoría creada exitosamente.', 'success')
        return redirect(url_for('categoria_rutas.crear_categoria_vista'))
    
    cuenta_id = request.args.get('cuenta_id', type=int)
    if cuenta_id:
        categorias = CategoriaServicio.obtener_categorias(cuenta_id)
    else:
        categorias = []
    return render_template('categorias.html', categorias=categorias)

@categoria_rutas.route('/categorias/actualizar/<int:categoria_id>', methods=['GET', 'POST'])
def actualizar_categoria_vista(categoria_id):
    categoria = CategoriaServicio.obtener_categorias(categoria_id)  # Puedes cambiarlo por get() ya que es por ID
    categoria = categoria[0] if isinstance(categoria, list) and categoria else None
    if not categoria:
        flash('Categoría no encontrada.', 'danger')
        return redirect(url_for('categoria_rutas.crear_categoria_vista'))
    
    if request.method == 'POST':
        nuevo_nombre = request.form.get('nombre')
        CategoriaServicio.actualizar_categoria(categoria_id, nuevo_nombre)
        flash('Categoría actualizada.', 'success')
        return redirect(url_for('categoria_rutas.crear_categoria_vista'))
    
    return render_template('categoria_actualizar.html', categoria=categoria)

@categoria_rutas.route('/categorias/eliminar/<int:categoria_id>', methods=['POST'])
def eliminar_categoria_vista(categoria_id):
    CategoriaServicio.eliminar_categoria(categoria_id)
    flash('Categoría eliminada.', 'success')
    return redirect(url_for('categoria_rutas.crear_categoria_vista'))
