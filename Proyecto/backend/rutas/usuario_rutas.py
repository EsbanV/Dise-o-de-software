from flask import Blueprint, request, session, jsonify, current_app

usuario_rutas = Blueprint('usuario_rutas', __name__)

@usuario_rutas.route('/', methods=['POST'])
def registrar_usuario():
    """
    summary: Registra un nuevo usuario.
    description: Crea un usuario con los datos recibidos en el body.
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            nombre: {type: string}
            correo: {type: string}
            contrasena: {type: string}
          required: [nombre, correo, contrasena]
    responses:
      200:
        description: Usuario registrado exitosamente.
        schema:
          type: object
          properties:
            success: {type: boolean}
            usuario:
              type: object
              properties:
                id: {type: integer}
                nombre: {type: string}
      400:
        description: Error en los datos enviados.
    """
    data = request.get_json()
    nombre = data.get('nombre')
    correo = data.get('correo')
    contrasena = data.get('contrasena')
    try:
        usuario = current_app.usuario_facade.registrar_usuario(nombre, correo, contrasena)
        return jsonify({'success': True, 'usuario': usuario.to_dict()}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@usuario_rutas.route('/login', methods=['POST'])
def login():
    """
    summary: Inicia sesión de usuario.
    description: Valida credenciales y activa la sesión.
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            correo: {type: string}
            contrasena: {type: string}
          required: [correo, contrasena]
    responses:
      200:
        description: Login exitoso.
      401:
        description: Credenciales inválidas.
      400:
        description: Error en la solicitud.
    """
    data = request.get_json()
    correo = data.get('correo')
    contrasena = data.get('contrasena')
    try:
        usuario = current_app.usuario_facade.iniciar_sesion(correo, contrasena)
        if usuario:
            session['usuario_id'] = usuario.id
            session['nombre'] = usuario.nombre
            session['logged_in'] = True
            return jsonify({'success': True, 'usuario': usuario.to_dict()}), 200
        else:
            return jsonify({'success': False, 'error': 'Credenciales inválidas.'}), 401
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@usuario_rutas.route('/logout', methods=['POST'])
def logout():
    """
    summary: Cierra sesión del usuario actual.
    description: Elimina los datos de sesión del usuario.
    responses:
      200:
        description: Sesión cerrada exitosamente.
      401:
        description: No había sesión activa.
    """
    session.pop('usuario_id', None)
    session.pop('nombre', None)
    session.pop('logged_in', None)
    return jsonify({'success': True, 'message': 'Sesión cerrada.'}), 200

@usuario_rutas.route('/<int:usuario_id>', methods=['GET'])
def obtener_usuario(usuario_id):
    """
    summary: Obtiene los datos de un usuario por su ID.
    description: Devuelve la información del usuario especificado.
    parameters:
      - in: path
        name: usuario_id
        type: integer
        required: true
    responses:
      200:
        description: Usuario encontrado.
        schema:
          type: object
          properties:
            id: {type: integer}
            nombre: {type: string}
            correo: {type: string}
      404:
        description: Usuario no encontrado.
    """
    try:
        usuario = current_app.usuario_facade.datos_usuario(usuario_id)
        return jsonify(usuario.to_dict()), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 404

@usuario_rutas.route('/session', methods=['GET'])
def verificar_sesion():
    """
    summary: Verifica si hay sesión activa.
    description: Devuelve el estado de la sesión y los datos del usuario si está autenticado.
    responses:
      200:
        description: Sesión activa.
        schema:
          type: object
          properties:
            loggedIn: {type: boolean}
            usuario:
              type: object
              properties:
                id: {type: integer}
                nombre: {type: string}
      401:
        description: No hay sesión activa.
    """
    usuario_id = session.get('usuario_id')
    if usuario_id:
        usuario = current_app.usuario_facade.datos_usuario(usuario_id)
        return jsonify({'loggedIn': True, 'usuario': usuario.to_dict()}), 200
    return jsonify({'loggedIn': False}), 401
