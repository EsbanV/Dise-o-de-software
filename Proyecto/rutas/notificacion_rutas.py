# routes/notificacion_routes.py
from flask import Blueprint, redirect, url_for
from servicios.notificacion_servicio import NotificacionService

notificacion_rutas = Blueprint('notificacion_rutas', __name__, url_prefix='/notificaciones')

@notificacion_rutas.route('/<int:notificacion_id>/leer', methods=['POST'])
def marcar_leida(notificacion_id):
    NotificacionService.marcar_como_leida(notificacion_id)
    return redirect(url_for('index_rutas.home'))
