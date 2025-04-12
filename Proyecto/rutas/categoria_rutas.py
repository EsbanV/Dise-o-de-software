from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, session
from servicios.categoria_servicio import CategoriaServicio

categoria_rutas = Blueprint('categoria_rutas', __name__)

@categoria_rutas.route('/categorias', methods=['POST'])
def crear_categoria_api():
    data = request.get_json()
    nombre = data.get('nombre')
    cuenta_id = data.get('cuenta_id')
    categoria = CategoriaServicio.crear_categoria(nombre, cuenta_id)
    return jsonify({"id": categoria.id, "nombre": categoria.nombre}), 201

@categoria_rutas.route('/categorias/<int:cuenta_id>', methods=['GET'])
def listar_categorias_api(cuenta_id):
    categorias = CategoriaServicio.obtener_categorias(cuenta_id)
    categorias_serializadas = [{"id": c.id, "nombre": c.nombre} for c in categorias]
    return jsonify(categorias_serializadas), 200

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
