from sqlalchemy.orm import joinedload
from sqlalchemy import extract
from servicios.base_datos import ServicioBaseDatos
from modelos.transaccion import Transaccion

class TransaccionRepositorio(ServicioBaseDatos):
    def obtener_por_cuenta_con_categoria(self, cuenta_id, limit=None, offset=0, year=None, month=None, day=None):
        query = (
            self.session.query(Transaccion)
            .options(joinedload(Transaccion.categoria))
            .filter_by(cuenta_bancaria_id=cuenta_id)
        )
        if year:
            query = query.filter(extract('year', Transaccion.fecha) == year)
        if month:
            query = query.filter(extract('month', Transaccion.fecha) == month)
        if day:
            query = query.filter(extract('day', Transaccion.fecha) == day)
        if limit is not None:
            query = query.offset(offset).limit(limit)
        return query.all()

    def obtener_con_filtro(self, modelo, filtros, limit=None, offset=0, year=None, month=None, day=None):
        query = self.session.query(modelo)
        if modelo is Transaccion:
            query = query.options(joinedload(Transaccion.categoria))
        for f in filtros:
            query = query.filter(f)
        if year:
            query = query.filter(extract('year', Transaccion.fecha) == year)
        if month:
            query = query.filter(extract('month', Transaccion.fecha) == month)
        if day:
            query = query.filter(extract('day', Transaccion.fecha) == day)
        if limit is not None:
            query = query.offset(offset).limit(limit)
        return query.all()

    def contar_transacciones(self, cuenta_id, year=None, month=None, day=None):
        query = self.session.query(Transaccion).filter(Transaccion.cuenta_bancaria_id == cuenta_id)
        if year:
            query = query.filter(extract('year', Transaccion.fecha) == year)
        if month:
            query = query.filter(extract('month', Transaccion.fecha) == month)
        if day:
            query = query.filter(extract('day', Transaccion.fecha) == day)
        return query.count()
