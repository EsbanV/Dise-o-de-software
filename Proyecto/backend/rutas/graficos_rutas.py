from flask import Blueprint, request, jsonify, session, current_app

graficos_rutas = Blueprint('graficos_rutas', __name__)

@graficos_rutas.route('/', methods=['GET'])
def obtener_datos_graficos_api():
    """
    summary: Obtiene los datos agregados y de categorías para los gráficos financieros.
    description: Devuelve los datos numéricos requeridos para construir los gráficos de ingresos, gastos y balance neto, filtrados por cuenta y por fecha.
    parameters:
      - in: query
        name: cuenta_id
        type: integer
        required: true
        description: ID de la cuenta bancaria.
      - in: query
        name: year
        type: integer
        required: false
      - in: query
        name: month
        type: integer
        required: false
      - in: query
        name: day
        type: integer
        required: false
    responses:
      200:
        description: Datos de gráficos obtenidos exitosamente.
        schema:
          type: object
          properties:
            datos_grafico: {type: object}
            datos_grafico_categoria: {type: array}
            datos_grafico_categoria_ingreso: {type: array}
      401:
        description: No autenticado.
      403:
        description: Cuenta no encontrada o no pertenece al usuario.
      500:
        description: Error interno.
    """
    usuario_id = session.get("usuario_id")
    if not usuario_id:
        return jsonify({'success': False, 'error': 'No autenticado.'}), 401

    cuenta_id = request.args.get('cuenta_id', type=int)
    year = request.args.get('year', type=int)
    month = request.args.get('month', type=int)
    day = request.args.get('day', type=int)

    if not cuenta_id:
        return jsonify({"success": False, "error": "ID de cuenta requerido"}), 400

    try:
        cuenta = current_app.cuenta_bancaria_facade.obtener_cuenta_por_id(cuenta_id)
        if cuenta is None or cuenta.usuario_id != usuario_id:
            return jsonify({"success": False, "error": "Cuenta no encontrada o no pertenece al usuario"}), 403

        if year is not None and month is not None and day is not None:
            datos_grafico = current_app.grafico_facade.obtener_datos_crudos_por_dia(cuenta_id, year, month, day)
            grafico_gastos_categoria = current_app.grafico_facade.obtener_datos_categorias_gasto_por_dia(cuenta_id, year, month, day)
            grafico_ingresos_categoria = current_app.grafico_facade.obtener_datos_categorias_ingreso_por_dia(cuenta_id, year, month, day)
        elif year is not None and month is not None:
            datos_grafico = current_app.grafico_facade.obtener_datos_crudos_por_mes(cuenta_id, year, month)
            grafico_gastos_categoria = current_app.grafico_facade.obtener_datos_categorias_gasto_por_mes(cuenta_id, year, month)
            grafico_ingresos_categoria = current_app.grafico_facade.obtener_datos_categorias_ingreso_por_mes(cuenta_id, year, month)
        elif year is not None:
            datos_grafico = current_app.grafico_facade.obtener_datos_crudos_por_anio(cuenta_id, year)
            grafico_gastos_categoria = current_app.grafico_facade.obtener_datos_categorias_gasto_por_anio(cuenta_id, year)
            grafico_ingresos_categoria = current_app.grafico_facade.obtener_datos_categorias_ingreso_por_anio(cuenta_id, year)
        else:
            datos_grafico = current_app.grafico_facade.obtener_datos_crudos(cuenta_id)
            grafico_gastos_categoria = current_app.grafico_facade.obtener_datos_categorias_gasto(cuenta_id)
            grafico_ingresos_categoria = current_app.grafico_facade.obtener_datos_categorias_ingreso(cuenta_id)

        return jsonify({
            "datos_grafico": datos_grafico,
            "datos_grafico_categoria": grafico_gastos_categoria,
            "datos_grafico_categoria_ingreso": grafico_ingresos_categoria,
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
