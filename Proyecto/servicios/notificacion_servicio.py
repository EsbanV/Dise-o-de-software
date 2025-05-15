# services/notificacion_service.py
from modelos.notificacion import Notificacion
from servicios.base_datos import ServicioBaseDatos
from flask import abort

class NotificacionService:
    @staticmethod
    def obtener_notificaciones(usuario_id: int):
        return Notificacion.query.filter_by(usuario_id=usuario_id).order_by(Notificacion.fecha_creacion.desc()).all()

    @staticmethod
    def marcar_como_leida(notificacion_id: int):
        notificacion = Notificacion.query.get_or_404(notificacion_id)
        notificacion.leida = True
        ServicioBaseDatos.agregar(notificacion)
        return notificacion
