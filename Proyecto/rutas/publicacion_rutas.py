from flask import Blueprint, request, jsonify, abort, current_app
from flask import Blueprint, render_template, request, redirect, url_for, session

publicacion_rutas = Blueprint('publicacion_rutas', __name__, url_prefix='/publicaciones', template_folder='../templates')

@publicacion_rutas.route('/nueva', methods=['GET'])
def nueva_publicacion():
    if not session.get('usuario_id'):
        return redirect(url_for('usuario_rutas.login'))
    return render_template('crear_publicacion.html')


@publicacion_rutas.route('', methods=['POST'])
def crear_publicacion():
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return redirect(url_for('usuario_rutas.login'))

    titulo    = request.form.get('titulo', '').strip()
    contenido = request.form.get('contenido', '').strip()
    if not (titulo and contenido):
        return render_template('crear_publicacion.html',
                               error="Faltan datos requeridos",
                               titulo=titulo,
                               contenido=contenido)
    try:
        current_app.comunidad_facade.crear_publicacion(usuario_id, titulo, contenido)
    except Exception as e:
        return render_template('crear_publicacion.html',
                               error=f"Error al crear la publicación: {e}",
                               titulo=titulo,
                               contenido=contenido)

    return redirect(url_for('publicacion_rutas.foro'))

@publicacion_rutas.route('', methods=['GET'])
def listar_publicaciones():
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return redirect(url_for('usuario_rutas.login'))

    try:
        publicaciones = current_app.comunidad_facade.obtener_publicaciones()
    except Exception as e:
        abort(500, f"Error al obtener publicaciones: {e}")

    resultado = [publicaciones.to_dict() for publicacion in publicaciones]
    return jsonify(resultado), 200

@publicacion_rutas.route('/foro')
def foro():
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return redirect(url_for('usuario_rutas.login'))
    
    try:
        publicaciones = current_app.comunidad_facade.obtener_publicaciones()
    except Exception as e:
        abort(500, f"Error al obtener publicaciones: {e}")

    return render_template('foro.html', publicaciones=publicaciones)

@publicacion_rutas.route('/<int:publicacion_id>', methods=['GET'])
def ver_publicacion(publicacion_id):

    publicacion = current_app.comunidad_facade.obtener_publicacion(publicacion_id)
    return render_template('publicacion_detalle.html', publicacion=publicacion)

@publicacion_rutas.route('/<int:publicacion_id>/comentarios', methods=['POST'])
def crear_comentario(publicacion_id):
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return redirect(url_for('usuario_rutas.login'))

    contenido = request.form.get('contenido', '').strip()
    if not contenido:
        return redirect(url_for('publicacion_rutas.ver_publicacion', publicacion_id=publicacion_id, _anchor='comments'))
    try:
        current_app.comunidad_facade.agregar_comentario(publicacion_id, usuario_id, contenido)
    except ValueError as e:
            return render_template('publicacion_detalle.html',
                                publicacion=current_app.comunidad_facade.obtener_publicacion(publicacion_id),
                                error=str(e))
    return redirect(url_for('publicacion_rutas.ver_publicacion', publicacion_id=publicacion_id, _anchor='comments'))
