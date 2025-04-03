from flask import Blueprint, request, jsonify
from servicios.categoria_servicio import CategoriaServicio

categoria_rutas = Blueprint('categoria_rutas', __name__)

@categoria_rutas.route('/categorias', methods=['POST'])
def crear_categoria():
    data = request.get_json()
    nombre = data.get('nombre')
    cuenta_id = data.get('cuenta_id')
    categoria = CategoriaServicio.crear_categoria(nombre, cuenta_id)
    return jsonify({"id": categoria.id, "nombre": categoria.nombre}), 201

@categoria_rutas.route('/categorias/<int:cuenta_id>', methods=['GET'])
def listar_categorias(cuenta_id):
    categorias = CategoriaServicio.obtener_categorias(cuenta_id)
    categorias_serializadas = [{"id": c.id, "nombre": c.nombre} for c in categorias]
    return jsonify(categorias_serializadas), 200
