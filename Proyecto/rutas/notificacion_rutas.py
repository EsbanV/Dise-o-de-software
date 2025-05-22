from flask import Blueprint, redirect, url_for, current_app

notificacion_rutas = Blueprint('notificacion_rutas', __name__, url_prefix='/notificaciones')

@notificacion_rutas.route('/<int:notificacion_id>/leer', methods=['POST'])
def marcar_leida(notificacion_id):
    current_app.notificacion_servicio.marcar_como_leida(notificacion_id)
    return redirect(url_for('index_rutas.home'))
