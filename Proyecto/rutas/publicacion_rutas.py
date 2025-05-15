from flask import Blueprint, request, jsonify, abort
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from servicios.publicacion_servicio import PublicacionService
from servicios.autor_servicio import AutorService  # si también notificas a seguidores

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

    PublicacionService.crear_publicacion(usuario_id, titulo, contenido)

    return redirect(url_for('publicacion_rutas.foro'))

@publicacion_rutas.route('', methods=['GET'])
def listar_publicaciones():
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return redirect(url_for('usuario_rutas.login'))

    try:
        publicaciones = PublicacionService.obtener_publicaciones()
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
        publicaciones = PublicacionService.obtener_publicaciones()
    except Exception as e:
        abort(500, f"Error al obtener publicaciones: {e}")

    return render_template('foro.html', publicaciones=publicaciones)

@publicacion_rutas.route('/<int:publicacion_id>', methods=['GET'])
def ver_publicacion(publicacion_id):

    publicacion = PublicacionService.obtener_publicacion_o_404(publicacion_id)
    return render_template('publicacion_detalle.html', publicacion=publicacion)

@publicacion_rutas.route('/<int:publicacion_id>/comentarios', methods=['POST'])
def crear_comentario(publicacion_id):
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return redirect(url_for('usuario_rutas.login'))

    contenido = request.form.get('contenido', '').strip()
    if not contenido:
        return redirect(url_for('publicacion_rutas.ver_publicacion', publicacion_id=publicacion_id, _anchor='comments'))

    PublicacionService.agregar_comentario(publicacion_id, usuario_id, contenido)

    return redirect(url_for('publicacion_rutas.ver_publicacion', publicacion_id=publicacion_id, _anchor='comments'))
