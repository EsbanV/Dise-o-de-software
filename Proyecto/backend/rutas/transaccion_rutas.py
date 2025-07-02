from flask import Blueprint, request, jsonify, session, current_app

transaccion_rutas = Blueprint('transaccion_rutas', __name__)

@transaccion_rutas.route('/', methods=['POST'])
def registrar_transaccion():
    """
    summary: Registra una transacción en una cuenta bancaria.
    description: Crea una transacción (gasto/ingreso) en la cuenta y categoría indicada.
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            cuenta_id: {type: integer}
            categoria_id: {type: integer}
            descripcion: {type: string}
            monto: {type: number}
          required: [cuenta_id, categoria_id, monto]
    responses:
      201:
        description: Transacción registrada correctamente.
        schema:
          type: object
          properties:
            success: {type: boolean}
            message: {type: string}
            nuevo_saldo: {type: number}
      400:
        description: Faltan campos obligatorios o error de negocio.
      401:
        description: No autenticado.
    """
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return jsonify({'success': False, 'error': 'Necesitas iniciar sesión para registrar transacciones.'}), 401
    data = request.get_json()
    cuenta_id = data.get('cuenta_id')
    categoria_id = data.get('categoria_id')
    descripcion = data.get('descripcion', '')
    monto = data.get('monto')
    try:
        transaccion = current_app.transaccion_facade.registrar_transaccion(
            cuenta_id, categoria_id, descripcion, monto, fecha=None
        )
        cuenta = current_app.cuenta_bancaria_facade.obtener_cuenta_por_id(cuenta_id)
        return jsonify({
            'success': True,
            'message': 'Transacción registrada correctamente.',
            'nuevo_saldo': cuenta.saldo if cuenta else None
        }), 201
    except Exception as e:
        return jsonify({'success': False, 'error': f'Error al registrar la transacción: {e}'}), 400

@transaccion_rutas.route('/', methods=['GET'])
def listar_transacciones():
    """
    summary: Lista las transacciones de una cuenta bancaria.
    description: Retorna todas las transacciones asociadas a una cuenta indicada por ID, con paginación.
    parameters:
      - in: query
        name: cuenta_id
        type: integer
        required: true
        description: ID de la cuenta bancaria
      - in: query
        name: limit
        type: integer
        required: false
        description: Cantidad máxima de transacciones a retornar (paginación)
      - in: query
        name: offset
        type: integer
        required: false
        description: Cantidad de transacciones a saltar (paginación)
    responses:
      200:
        description: Lista de transacciones obtenida correctamente.
        schema:
          type: object
          properties:
            success: {type: boolean}
            transacciones:
              type: array
              items:
                type: object
                properties:
                  id: {type: integer}
                  cuenta_id: {type: integer}
                  categoria_id: {type: integer}
                  descripcion: {type: string}
                  monto: {type: number}
                  fecha: {type: string}
            total: {type: integer}
      400:
        description: Falta el ID de la cuenta.
      401:
        description: No autenticado.
    """
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return jsonify({'success': False, 'error': 'Necesitas iniciar sesión.'}), 401

    cuenta_id = request.args.get('cuenta_id', type=int)
    if not cuenta_id:
        return jsonify({'success': False, 'error': 'Falta el ID de la cuenta.'}), 400

    limit = request.args.get('limit', default=20, type=int)
    offset = request.args.get('offset', default=0, type=int)

    # Nuevos filtros de fecha
    year = request.args.get('year', type=int)
    month = request.args.get('month', type=int)
    day = request.args.get('day', type=int)

    try:
        # Pasa los filtros al servicio
        transacciones = current_app.transaccion_facade.obtener_transacciones_por_cuenta(
            cuenta_id, limit=limit, offset=offset, year=year, month=month, day=day
        )
        data = [t.to_dict() for t in transacciones]
        total = current_app.transaccion_facade.contar_transacciones(
            cuenta_id, year=year, month=month, day=day
        )
        return jsonify({'success': True, 'transacciones': data, 'total': total}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': f'Error al listar transacciones: {e}'}), 500