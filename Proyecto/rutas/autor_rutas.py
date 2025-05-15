from flask import Blueprint, session, redirect, url_for, abort, request
from servicios.autor_servicio import AutorService

autor_rutas = Blueprint('autor_rutas', __name__, url_prefix='/autores')

@autor_rutas.route('/<int:autor_id>/suscribir', methods=['POST'])
def suscribir_autor(autor_id):
    subscriber_id = session.get('usuario_id')
    if not subscriber_id:
        return redirect(url_for('usuario_rutas.login'))

    try:
        AutorService.suscribir(subscriber_id, autor_id)
    except Exception as e:
        abort(400, str(e))

    publicacion_id = request.args.get('from_pub', type=int)
    if publicacion_id:
        return redirect(url_for('publicacion_rutas.ver_publicacion',
                                publicacion_id=publicacion_id))

    return redirect(url_for('publicacion_rutas.foro'))

@autor_rutas.route('/<int:autor_id>/desuscribir', methods=['POST'])
def desuscribir_autor(autor_id):
    subscriber_id = session.get('usuario_id')
    if not subscriber_id:
        return redirect(url_for('usuario_rutas.login'))

    try:
        AutorService.desuscribir(subscriber_id, autor_id)
    except Exception as e:
        abort(400, str(e))

    publicacion_id = request.args.get('from_pub', type=int)
    if publicacion_id:
        return redirect(url_for('publicacion_rutas.ver_publicacion',
                                publicacion_id=publicacion_id))

    return redirect(url_for('publicacion_rutas.foro'))
