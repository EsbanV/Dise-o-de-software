from config.config import db

class ServicioBaseDatos:
    @staticmethod
    def agregar(instancia):
        try:
            db.session.add(instancia)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def actualizar():
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def eliminar(instancia):
        try:
            db.session.delete(instancia)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def obtener_todos(modelo):
        return modelo.query.all()

    @staticmethod
    def obtener_por_id(modelo, id_):
        return modelo.query.get(id_)
