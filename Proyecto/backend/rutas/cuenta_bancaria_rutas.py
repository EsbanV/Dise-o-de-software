from flask import Blueprint, request, jsonify, session, current_app
from flasgger import swag_from

cuenta_rutas = Blueprint('cuenta_rutas', __name__)

@cuenta_rutas.route('/', methods=['GET'])
def obtener_cuentas():
    """
    summary: Lista las cuentas bancarias del usuario autenticado.
    description: |
        Retorna todas las cuentas bancarias asociadas al usuario autenticado.
    responses:
        200:
            description: Lista de cuentas obtenida exitosamente.
            schema:
                type: object
                properties:
                    success: {type: boolean}
                    cuentas:
                        type: array
                        items:
                            type: object
                            properties:
                                id: {type: integer}
                                nombre: {type: string}
                                saldo: {type: number}
        401:
            description: El usuario no ha iniciado sesión.
    """
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return jsonify({'success': False, 'error': 'Necesitas iniciar sesión para ver tus cuentas.'}), 401
    try:
        cuentas = current_app.cuenta_bancaria_facade.obtener_cuentas(usuario_id)
        cuentas_json = [c.to_dict() for c in cuentas]
        return jsonify({'success': True, 'cuentas': cuentas_json}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': 'Ocurrió un error interno'}), 500

@cuenta_rutas.route('/', methods=['POST'])
def crear_cuenta():
    """
    summary: Crea una nueva cuenta bancaria para el usuario autenticado.
    description: |
        Permite crear una cuenta bancaria nueva asociada al usuario autenticado.
    parameters:
      - in: body
        name: body
        required: true
        schema:
            type: object
            properties:
                nombre: {type: string}
                saldo_inicial: {type: number}
            required: [nombre]
    responses:
        201:
            description: Cuenta creada exitosamente.
            schema:
                type: object
                properties:
                    success: {type: boolean}
                    cuenta:
                        type: object
                        properties:
                            id: {type: integer}
                            nombre: {type: string}
                            saldo: {type: number}
        400:
            description: Datos de entrada inválidos.
        401:
            description: El usuario no ha iniciado sesión.
    """
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return jsonify({'success': False, 'error': 'Necesitas iniciar sesión para crear una cuenta.'}), 401
    data = request.get_json()
    nombre = data.get('nombre')
    saldo_inicial = data.get('saldo_inicial', 0)
    try:
        cuenta = current_app.cuenta_bancaria_facade.crear_cuenta(nombre, saldo_inicial, usuario_id)
        return jsonify({'success': True, 'cuenta': cuenta.to_dict()}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': 'No se pudo crear la cuenta.'}), 400

@cuenta_rutas.route('/<int:cuenta_id>', methods=['GET'])
def obtener_cuenta(cuenta_id):
    """
    summary: Obtiene una cuenta bancaria por su ID.
    description: |
        Retorna la información de la cuenta bancaria especificada, si pertenece al usuario autenticado.
    parameters:
      - in: path
        name: cuenta_id
        type: integer
        required: true
        description: ID de la cuenta bancaria
    responses:
        200:
            description: Cuenta obtenida exitosamente.
            schema:
                type: object
                properties:
                    success: {type: boolean}
                    cuenta:
                        type: object
                        properties:
                            id: {type: integer}
                            nombre: {type: string}
                            saldo: {type: number}
        401:
            description: El usuario no ha iniciado sesión.
        404:
            description: Cuenta no encontrada.
    """
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return jsonify({'success': False, 'error': 'Necesitas iniciar sesión.'}), 401
    try:
        cuenta = current_app.cuenta_bancaria_facade.obtener_cuenta_por_id(cuenta_id)
        if not cuenta:
            return jsonify({'success': False, 'error': 'Cuenta no encontrada.'}), 404
        return jsonify({'success': True, 'cuenta': cuenta.to_dict()}), 200
    except Exception:
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500

@cuenta_rutas.route('/<int:cuenta_id>', methods=['PUT'])
def actualizar_cuenta(cuenta_id):
    """
    summary: Actualiza una cuenta bancaria existente.
    description: Actualiza el nombre o el saldo de una cuenta bancaria existente, si pertenece al usuario autenticado.
    parameters:
      - in: path
        name: cuenta_id
        type: integer
        required: true
      - in: body
        name: body
        schema:
            type: object
            properties:
                nombre: {type: string}
                saldo: {type: number}
    responses:
        200:
            description: Cuenta actualizada exitosamente.
        400:
            description: Error en los datos enviados.
        401:
            description: El usuario no ha iniciado sesión.
        404:
            description: Cuenta no encontrada.
    """
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return jsonify({'success': False, 'error': 'Necesitas iniciar sesión.'}), 401
    data = request.get_json()
    nombre = data.get('nombre')
    saldo = data.get('saldo')
    try:
        cuenta = current_app.cuenta_bancaria_facade.obtener_cuenta_por_id(cuenta_id)
        if not cuenta:
            return jsonify({'success': False, 'error': 'Cuenta no encontrada.'}), 404
        current_app.cuenta_bancaria_facade.actualizar_cuenta(cuenta_id, nombre, saldo)
        return jsonify({'success': True, 'message': 'Cuenta actualizada exitosamente.'}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': 'No se pudo actualizar la cuenta.'}), 400

@cuenta_rutas.route('/<int:cuenta_id>', methods=['DELETE'])
def eliminar_cuenta(cuenta_id):
    """
    summary: Elimina una cuenta bancaria.
    description: Elimina la cuenta bancaria indicada por ID, si pertenece al usuario autenticado.
    parameters:
      - in: path
        name: cuenta_id
        type: integer
        required: true
    responses:
        200:
            description: Cuenta eliminada exitosamente.
        401:
            description: El usuario no ha iniciado sesión.
        404:
            description: Cuenta no encontrada.
        400:
            description: Error al eliminar la cuenta.
    """
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return jsonify({'success': False, 'error': 'Necesitas iniciar sesión.'}), 401
    try:
        current_app.cuenta_bancaria_facade.eliminar_cuenta(cuenta_id)
        return jsonify({'success': True, 'message': 'Cuenta eliminada.'}), 200
    except Exception:
        return jsonify({'success': False, 'error': 'No se pudo eliminar la cuenta.'}), 400

@cuenta_rutas.route('/<int:cuenta_id>/categorias', methods=['GET'])
def categorias_por_cuenta(cuenta_id):
    """
    summary: Lista las categorías asociadas a una cuenta bancaria.
    description: Devuelve todas las categorías asociadas a la cuenta bancaria indicada por ID.
    parameters:
      - in: path
        name: cuenta_id
        type: integer
        required: true
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
        401:
            description: El usuario no ha iniciado sesión.
    """
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return jsonify({'success': False, 'error': 'Necesitas iniciar sesión.'}), 401
    try:
        categorias = current_app.categoria_facade.obtener_categorias(cuenta_id)
        lista = [c.to_dict() for c in categorias]
        return jsonify({'success': True, 'categorias': lista}), 200
    except Exception:
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500

