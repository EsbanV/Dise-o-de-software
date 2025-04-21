from servicios.base_datos import ServicioBaseDatos
from modelos.categoria import Categoria, TipoCategoria
from modelos.transaccion import Transaccion
from modelos.cuenta_bancaria import CuentaBancaria



class GraficoServicio:
    @staticmethod
    def obtener_datos_crudos(cuenta_id):
        cuenta = ServicioBaseDatos.obtener_por_id(CuentaBancaria, cuenta_id)
        if not cuenta:
            return {
                'ingresos': 0,
                'gastos': 0,
                'balance_neto': 0
            }

        transacciones = ServicioBaseDatos.obtener_con_filtro(
            Transaccion,
            [Transaccion.cuenta_bancaria_id == cuenta.id]
        )

        ingresos = 0
        gastos = 0

        for t in transacciones:
            categoria = ServicioBaseDatos.obtener_por_id(Categoria, t.categoria_id)
            t.categoria = categoria

            if categoria:
                if categoria.tipo == TipoCategoria.INGRESO:
                    ingresos += abs(t.monto)
                elif categoria.tipo == TipoCategoria.GASTO:
                    gastos += abs(t.monto)
                else:
                    # Tipo desconocido
                    if t.monto > 0:
                        ingresos += t.monto
                    else:
                        gastos += abs(t.monto)
            else:
                if t.monto > 0:
                    ingresos += t.monto
                else:
                    gastos += abs(t.monto)

        return {
            'ingresos': round(ingresos, 2),
            'gastos': round(gastos, 2),
            'balance_neto': round(ingresos - gastos, 2)
        }

    @staticmethod
    def obtener_datos_categorias_gasto(cuenta_id):
        categorias = ServicioBaseDatos.obtener_con_filtro(
            Categoria,
            [Categoria.cuenta_id == cuenta_id, Categoria.tipo == TipoCategoria.GASTO]
        )

        datos = []

        for categoria in categorias:
            transacciones = ServicioBaseDatos.obtener_con_filtro(
                Transaccion,
                [Transaccion.categoria_id == categoria.id]
            )

            monto_total = sum(abs(t.monto) for t in transacciones)
            if monto_total > 0:
                datos.append({
                    'nombre': categoria.nombre or "Sin Nombre",
                    'tipo': categoria.tipo.value,
                    'total': monto_total or 0
                })

        return datos