from configuracion.extensiones import db

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
    def actualizar(instancia):
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
    
    @staticmethod
    def obtener_con_filtro(modelo, condiciones=[]):
        return modelo.query.filter(*condiciones).all()
    
    @staticmethod
    def obtener_unico_con_filtro(modelo, condiciones=[]):
        return modelo.query.filter(*condiciones).first()

