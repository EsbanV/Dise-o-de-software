from flask import Blueprint, jsonify, session, current_app, request

notificacion_rutas = Blueprint('notificacion_rutas', __name__, url_prefix='/api/notificaciones')

@notificacion_rutas.route('/<int:notificacion_id>', methods=['PATCH'])
def marcar_leida(notificacion_id):
    """
    summary: Marca una notificación como leída o no leída.
    description: Actualiza el estado de lectura de una notificación del usuario autenticado.
    parameters:
      - in: path
        name: notificacion_id
        type: integer
        required: true
        description: ID de la notificación
      - in: body
        name: body
        schema:
          type: object
          properties:
            leida: {type: boolean}
          required: []
    responses:
      200:
        description: Notificación marcada correctamente.
        schema:
          type: object
          properties:
            success: {type: boolean}
            message: {type: string}
            notificacion_id: {type: integer}
      400:
        description: Error en la petición.
      401:
        description: No autenticado.
    """
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return jsonify({'success': False, 'error': 'No autenticado.'}), 401

    data = request.get_json(silent=True) or {}
    print("Body recibido:", data)
    leida = data.get('leida', True)

    try:
        current_app.comunidad_facade.marcar_notificacion_leida(notificacion_id, leida)
        return jsonify({
            'success': True,
            'message': f'Notificación marcada como {"leída" if leida else "no leída"}.',
            'notificacion_id': notificacion_id
        }), 200
    except Exception as e:
        print("Error al marcar como leída:", e)
        return jsonify({'success': False, 'error': str(e)}), 400

@notificacion_rutas.route('/', methods=['GET'])
def obtener_notificaciones():
    """
    summary: Retorna la lista de notificaciones para el usuario autenticado.
    responses:
      200:
        description: Lista de notificaciones retornada correctamente.
      401:
        description: No autenticado.
    """
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return jsonify({'success': False, 'error': 'No autenticado.'}), 401

    try:
        notificaciones = current_app.comunidad_facade.obtener_notificaciones(usuario_id)
        notificaciones_json = [
            n.to_dict() if hasattr(n, 'to_dict') else {
                'id': n.id,
                'mensaje': getattr(n, 'mensaje', ''),
                'leido': getattr(n, 'leido', False)
            }
            for n in notificaciones
        ]
        return jsonify({'success': True, 'notificaciones': notificaciones_json}), 200
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': f'Ocurrió un error interno: {str(e)}'}), 500