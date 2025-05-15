# services/autor_service.py
from flask import abort
from configuracion.extensiones import db
from modelos.usuario import Usuario
from modelos.suscripcion_autor import SuscripcionAutor
from observers.observer import NotificationObserver
from servicios.base_datos import ServicioBaseDatos
from servicios.usuario_servicio import UsuarioServicio

class AutorService:

    confirmation_observers = [NotificationObserver()]
    author_observers = [NotificationObserver()]

    @staticmethod
    def suscribir(subscriber_id: int, autor_id: int):
        if subscriber_id == autor_id:
            abort(400, "No puedes suscribirte a ti mismo")
        suscripcion = SuscripcionAutor.query.get((subscriber_id, autor_id))
        if suscripcion:
            return suscripcion
        
        suscriptor = UsuarioServicio.obtener_usuario_activo_por_id(subscriber_id)
        autor = UsuarioServicio.obtener_usuario_activo_por_id(autor_id)

        suscripcion = SuscripcionAutor(subscriber_id=subscriber_id, autor_id=autor_id)
        ServicioBaseDatos.agregar(suscripcion)

        texto_autor = f"{suscriptor.nombre} te ha seguido"
        for obs in AutorService.author_observers:
            obs.update(
                subject=autor,
                evento='new_subscription_author',
                mensaje={'mensaje': texto_autor}
            )

        texto_subs = f"Te has suscrito a {autor.nombre}"
        for obs in AutorService.confirmation_observers:
            obs.update(
                subject=suscriptor,
                evento='new_subscription_confirmation',
                mensaje={'mensaje': texto_subs,
                         'target_user_id': suscriptor.id}
            )

        return suscripcion

    @staticmethod
    def desuscribir(subscriber_id: int, autor_id: int):

        suscripcion = SuscripcionAutor.query.get((subscriber_id, autor_id))
        if not suscripcion:
            abort(400, "No estabas suscrito a este autor")

        ServicioBaseDatos.eliminar(suscripcion)
        return