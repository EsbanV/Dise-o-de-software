# services/observer.py (continúa)

from configuracion.extensiones import db
from observers.iObserver import Observer
from modelos.usuario import Usuario
from modelos.notificacion import Notificacion
from servicios.base_datos import ServicioBaseDatos
from flask import current_app

class NotificationObserver(Observer):
    def update(self, subject, evento: str, mensaje: dict):

        current_app.logger.debug(f"[NotificationObserver] evento={evento}, subject={subject}, mensaje={mensaje}")

        if evento == 'comment':
            targets = [subject.usuario_id]
        elif evento == 'new_post':
            targets = [sa.subscriber_id for sa in subject.usuario.seguidores]

        elif evento == 'new_subscription_author':
            targets = [subject.id]

        elif evento == 'new_subscription_confirmation':
            targets = [mensaje['target_user_id']]
        else:
            return

        errores = []
        for uid in targets:
            noti = Notificacion(mensaje=mensaje['mensaje'], usuario_id=uid)
            try:
                ServicioBaseDatos.agregar(noti)
            except Exception as e:
                errores.append((uid, str(e)))

        if errores:
            for uid, err in errores:
                print(f"[ERROR] Falló notificación para usuario {uid}: {err}")