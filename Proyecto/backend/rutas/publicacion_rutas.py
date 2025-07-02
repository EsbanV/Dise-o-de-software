from flask import Blueprint, request, jsonify, session, current_app

publicacion_rutas = Blueprint('publicacion_rutas', __name__, url_prefix='/api/publicaciones')

@publicacion_rutas.route('/', methods=['POST'])
def crear_publicacion():
    """
    summary: Crea una nueva publicación en el foro.
    description: Permite a un usuario autenticado crear una publicación.
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            titulo: {type: string}
            contenido: {type: string}
          required: [titulo, contenido]
    responses:
      201:
        description: Publicación creada exitosamente.
        schema:
          type: object
          properties:
            success: {type: boolean}
            message: {type: string}
            publicacion_id: {type: integer}
      400:
        description: Faltan datos requeridos o error en la creación.
      401:
        description: No autenticado.
    """
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return jsonify({'success': False, 'error': 'No autenticado.'}), 401

    data = request.get_json()
    titulo = data.get('titulo', '').strip()
    contenido = data.get('contenido', '').strip()
    if not (titulo and contenido):
        return jsonify({'success': False, 'error': 'Faltan datos requeridos.'}), 400
    try:
        publicacion = current_app.comunidad_facade.crear_publicacion(usuario_id, titulo, contenido)
        return jsonify({'success': True, 'message': 'Publicación creada.', 'publicacion_id': publicacion.id}), 201
    except Exception as e:
        print("watafak")
        return jsonify({'success': False, 'error': f'Error al crear la publicación: {e}'}), 400

@publicacion_rutas.route('/', methods=['GET'])
def listar_publicaciones():
    """
    summary: Lista todas las publicaciones del foro (con paginación).
    description: Permite obtener publicaciones paginadas.
    parameters:
      - in: query
        name: limit
        type: integer
        required: false
        default: 10
      - in: query
        name: offset
        type: integer
        required: false
        default: 0
    responses:
      200:
        description: Publicaciones obtenidas correctamente.
        schema:
          type: object
          properties:
            success: {type: boolean}
            publicaciones:
              type: array
              items:
                type: object
            total: {type: integer}
      401:
        description: No autenticado.
      500:
        description: Error interno.
    """
    usuario_id_session = session.get('usuario_id')
    if not usuario_id_session:
        return jsonify({'success': False, 'error': 'No autenticado.'}), 401

    usuario_id = request.args.get('usuario_id', type=int)
    print(f"Query param usuario_id: {usuario_id}")
    limit = request.args.get('limit', default=10, type=int)
    offset = request.args.get('offset', default=0, type=int)
    try:
        if usuario_id:
            print("Filtrando publicaciones por usuario:", usuario_id)
            publicaciones, total = current_app.comunidad_facade.obtener_publicaciones_por_usuario(
                usuario_id=usuario_id, limit=limit, offset=offset
            )
        else:
            print("Trayendo todas las publicaciones (no filtrado por usuario)")
            publicaciones, total = current_app.comunidad_facade.obtener_publicaciones(limit=limit, offset=offset)

        resultado = [p.to_dict() for p in publicaciones]
        return jsonify({'success': True, 'publicaciones': resultado, 'total': total}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': f'Error al obtener publicaciones: {e}'}), 500

@publicacion_rutas.route('/<int:publicacion_id>', methods=['GET'])
def obtener_publicacion(publicacion_id):
    """
    summary: Obtiene una publicación por ID junto a sus comentarios.
    description: Devuelve la publicación y todos sus comentarios.
    parameters:
      - in: path
        name: publicacion_id
        type: integer
        required: true
    responses:
      200:
        description: Publicación encontrada.
        schema:
          type: object
          properties:
            success: {type: boolean}
            publicacion:
              type: object
      401:
        description: No autenticado.
      404:
        description: Publicación no encontrada.
    """
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return jsonify({'success': False, 'error': 'No autenticado.'}), 401
    try:
        publicacion = current_app.comunidad_facade.obtener_publicacion(publicacion_id)
        comentarios = [c.to_dict() for c in getattr(publicacion, "comentarios", [])]
        pub_dict = publicacion.to_dict()
        pub_dict["comentarios"] = comentarios
        return jsonify({'success': True, 'publicacion': pub_dict}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': f'Error al obtener la publicación: {e}'}), 404

@publicacion_rutas.route('/<int:publicacion_id>/comentarios', methods=['POST'])
def crear_comentario(publicacion_id):
    """
    summary: Crea un comentario en una publicación.
    description: Permite a un usuario autenticado comentar en una publicación existente.
    parameters:
      - in: path
        name: publicacion_id
        type: integer
        required: true
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            contenido: {type: string}
          required: [contenido]
    responses:
      201:
        description: Comentario agregado correctamente.
        schema:
          type: object
          properties:
            success: {type: boolean}
            message: {type: string}
            comentario: {type: object}
      400:
        description: Faltan datos requeridos o error en la creación.
      401:
        description: No autenticado.
    """
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return jsonify({'success': False, 'error': 'No autenticado.'}), 401

    data = request.get_json()
    contenido = data.get('contenido', '').strip()
    if not contenido:
        return jsonify({'success': False, 'error': 'Falta el contenido del comentario.'}), 400
    try:
        comentario = current_app.comunidad_facade.agregar_comentario(publicacion_id, usuario_id, contenido)
        return jsonify({'success': True, 'message': 'Comentario agregado.', 'comentario': comentario.to_dict()}), 201
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': f'Error al agregar comentario: {e}'}), 400
