from flask import Blueprint, session, request, jsonify, current_app

autor_rutas = Blueprint('autor_rutas', __name__, url_prefix='/api/autores')

@autor_rutas.route('/<int:autor_id>/suscriptores', methods=['POST'])
def suscribir_autor(autor_id):
    """
    summary: Suscribe al usuario autenticado a un autor.
    description: El usuario autenticado se suscribe a las publicaciones de otro autor.
    parameters:
      - in: path
        name: autor_id
        type: integer
        required: true
        description: ID del autor al que suscribirse
      - in: query
        name: from_pub
        type: integer
        required: false
        description: ID de la publicación desde donde se realiza la suscripción (opcional)
    responses:
      200:
        description: Suscripción realizada correctamente.
        schema:
          type: object
          properties:
            success: {type: boolean}
            message: {type: string}
            autor_id: {type: integer}
            from_publicacion_id: {type: integer}
      401:
        description: No autenticado.
      400:
        description: Error en la suscripción.
    """
    subscriber_id = session.get('usuario_id')
    if not subscriber_id:
        return jsonify({'success': False, 'error': 'No autenticado.'}), 401

    try:
        current_app.comunidad_facade.suscribirse_autor(subscriber_id, autor_id)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

    publicacion_id = request.args.get('from_pub', type=int)
    return jsonify({
        'success': True,
        'message': 'Suscripción realizada correctamente.',
        'autor_id': autor_id,
        'from_publicacion_id': publicacion_id
    }), 200

@autor_rutas.route('/<int:autor_id>/suscriptores', methods=['DELETE'])
def desuscribir_autor(autor_id):
    """
    summary: El usuario autenticado cancela la suscripción a un autor.
    description: El usuario autenticado se desuscribe de las publicaciones de un autor.
    parameters:
      - in: path
        name: autor_id
        type: integer
        required: true
        description: ID del autor a desuscribirse
      - in: query
        name: from_pub
        type: integer
        required: false
        description: ID de la publicación desde donde se realiza la desuscripción (opcional)
    responses:
      200:
        description: Desuscripción realizada correctamente.
        schema:
          type: object
          properties:
            success: {type: boolean}
            message: {type: string}
            autor_id: {type: integer}
            from_publicacion_id: {type: integer}
      401:
        description: No autenticado.
      400:
        description: Error en la desuscripción.
    """
    subscriber_id = session.get('usuario_id')
    if not subscriber_id:
        return jsonify({'success': False, 'error': 'No autenticado.'}), 401

    try:
        current_app.comunidad_facade.desuscribirse_autor(subscriber_id, autor_id)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

    publicacion_id = request.args.get('from_pub', type=int)
    return jsonify({
        'success': True,
        'message': 'Desuscripción realizada correctamente.',
        'autor_id': autor_id,
        'from_publicacion_id': publicacion_id
    }), 200
