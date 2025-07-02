from flask import Blueprint, request, jsonify, session, current_app
from flasgger import swag_from

categoria_rutas = Blueprint('categoria_rutas', __name__)

@categoria_rutas.route('/', methods=['POST'])
def crear_categoria():
    """
    summary: Crea una nueva categoría en una cuenta bancaria.
    description: |
        Permite crear una nueva categoría (gasto o ingreso) en una cuenta bancaria del usuario autenticado.
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            cuenta_id: {type: integer}
            nombre: {type: string}
            tipo: {type: string}
            presupuesto: {type: number}
          required: [cuenta_id, nombre, tipo]
    responses:
      201:
        description: Categoría creada exitosamente.
        schema:
          type: object
          properties:
            success: {type: boolean}
            id: {type: integer}
            nombre: {type: string}
      400:
        description: Error en los datos enviados.
      401:
        description: No autenticado.
    """
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return jsonify({'success': False, 'error': 'Inicia sesión para continuar.'}), 401
    data = request.get_json()
    cuenta_id = data.get('cuenta_id')
    nombre = data.get('nombre')
    tipo = data.get('tipo')
    print(f"DEBUG tipo recibido: {repr(tipo)}")
    presupuesto = data.get('presupuesto')

    try:
        categoria = current_app.categoria_facade.crear_categoria(cuenta_id=cuenta_id, nombre=nombre, tipo=tipo, presupuesto=presupuesto)
        return jsonify({'success': True, 'id': categoria.id, 'nombre': categoria.nombre}), 201
    except ValueError as e:
        mensaje = str(e)
        print(mensaje)
        # Personaliza el error del límite de categorías
        if 'más de 8 categorías' in mensaje:
            return jsonify({
                'success': False,
                'error': 'La categoría no ha sido creada, razón: excede máximo categorías (max: 8)'
            }), 400
        # Otros errores controlados
        return jsonify({'success': False, 'error': mensaje}), 400
    except Exception as e:
        # No devuelvas errores internos, solo loguea
        current_app.logger.error(f'Error interno creando categoría: {e}')
        return jsonify({'success': False, 'error': 'Error interno, contacta al administrador.'}), 500

@categoria_rutas.route('/', methods=['GET'])
def listar_categorias():
    """
    summary: Lista todas las categorías filtradas por cuenta y tipo.
    description: Retorna todas las categorías de una cuenta bancaria, opcionalmente filtradas por tipo.
    parameters:
      - in: query
        name: cuenta_id
        type: integer
        required: false
        description: ID de la cuenta bancaria a filtrar
      - in: query
        name: tipo
        type: string
        required: false
        description: Tipo de la categoría (ejemplo: 'ingreso', 'gasto')
    responses:
      200:
        description: Categorías obtenidas exitosamente.
        schema:
          type: object
          properties:
            success: {type: boolean}
            categorias:
              type: array
              items:
                type: object
                properties:
                  id: {type: integer}
                  nombre: {type: string}
                  tipo: {type: string}
                  presupuesto: {type: number}
      401:
        description: No autenticado.
    """
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return jsonify({'success': False, 'error': 'Inicia sesión para continuar.'}), 401
    cuenta_id = request.args.get('cuenta_id', type=int)
    tipo = request.args.get('tipo')
    try:
        categorias = current_app.categoria_facade.obtener_categorias_filtradas(cuenta_id, tipo)
        data = [c.to_dict() for c in categorias]
        return jsonify({'success': True, 'categorias': data}), 200
    except Exception:
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500

@categoria_rutas.route('/<int:categoria_id>', methods=['PUT'])
def actualizar_categoria(categoria_id):
    """
    summary: Actualiza el nombre de una categoría.
    description: Modifica el nombre de una categoría existente.
    parameters:
      - in: path
        name: categoria_id
        type: integer
        required: true
      - in: body
        name: body
        schema:
          type: object
          properties:
            nombre: {type: string}
    responses:
      200:
        description: Categoría actualizada exitosamente.
      400:
        description: Error en los datos enviados.
      401:
        description: No autenticado.
      404:
        description: Categoría no encontrada.
    """
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return jsonify({'success': False, 'error': 'Inicia sesión para continuar.'}), 401
    data = request.get_json()
    nombre = data.get('nombre')
    try:
        categoria = current_app.categoria_facade.obtener_categoria_por_id(categoria_id)
        if not categoria:
            return jsonify({'success': False, 'error': 'Categoría no encontrada.'}), 404
        current_app.categoria_facade.actualizar_categoria(categoria_id, nombre)
        return jsonify({'success': True, 'message': 'Categoría actualizada.'}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@categoria_rutas.route('/<int:categoria_id>', methods=['DELETE'])
def eliminar_categoria(categoria_id):
    """
    summary: Elimina una categoría.
    description: Elimina la categoría indicada por ID.
    parameters:
      - in: path
        name: categoria_id
        type: integer
        required: true
    responses:
      200:
        description: Categoría eliminada exitosamente.
      401:
        description: No autenticado.
      404:
        description: Categoría no encontrada.
      400:
        description: Error al eliminar la categoría.
    """
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return jsonify({'success': False, 'error': 'Inicia sesión para continuar.'}), 401
    try:
        categoria = current_app.categoria_facade.obtener_categoria_por_id(categoria_id)
        if not categoria:
            return jsonify({'success': False, 'error': 'Categoría no encontrada.'}), 404
        current_app.categoria_facade.eliminar_categoria(categoria_id)
        return jsonify({'success': True, 'message': 'Categoría eliminada.'}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400
