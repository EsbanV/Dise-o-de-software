from flask import Blueprint, request, jsonify, session, current_app
from datetime import datetime, timedelta
from functools import wraps

def login_requerido_api(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("usuario_id"):
            return jsonify({"error": "Sesión no válida"}), 401
        return f(*args, **kwargs)
    return wrapper

api_rutas = Blueprint('api_rutas', __name__)

@api_rutas.route('/categorias', methods=['POST'])
@login_requerido_api
def crear_categoria():

    data = request.json
    try:
        nombre = data.get("nombre")
        tipo = data.get("tipo")
        cuenta_id = int(data.get("cuenta_id"))
        presupuesto = data.get("presupuesto")

        nueva_categoria = current_app.categoria_facade.crear_categoria(nombre, tipo, presupuesto, cuenta_id)
        return jsonify({"success": True, "id": nueva_categoria.id, "nombre": nueva_categoria.nombre}), 201

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@api_rutas.route('/cuentas', methods=['POST'])
@login_requerido_api
def crear_cuenta_json():
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return jsonify({"error": "Sesión expirada"}), 401
    data = request.get_json()

    nombre = data.get('nombre')
    saldo_inicial = data.get('saldo_inicial')

    try:
        saldo_inicial = float(saldo_inicial)
    except (TypeError, ValueError):
        return jsonify({"error": "Saldo inválido"}), 400

    if not nombre or not usuario_id:
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    cuenta = current_app.cuenta_bancaria_facade.crear_cuenta(nombre, saldo_inicial, usuario_id)
    return jsonify({
        "mensaje": "Cuenta creada correctamente",
        "cuenta": {
            "id": cuenta.id,
            "nombre": cuenta.nombre,
            "saldo": cuenta.saldo
        }
    }), 201

@api_rutas.route('/categorias', methods=['GET'])
@login_requerido_api
def obtener_categorias():
    cuenta_id = request.args.get('cuenta_id', type=int)
    tipo = request.args.get('tipo')

    print("✅ Entrando a /api/categorias con cuenta:", cuenta_id, "tipo:", tipo)

    if not cuenta_id:
        print("❌ Falta cuenta_id")
        return jsonify({"error": "Falta el ID de la cuenta"}), 400

    categorias = current_app.categoria_facade.obtener_categorias_filtradas(cuenta_id, tipo)
    print("✅ Categorías obtenidas:", categorias)

    data = [
        {
            "id": c.id,
            "nombre": c.nombre,
            "tipo": c.tipo.value
        } for c in categorias
    ]

    print("📤 Datos a devolver:", data)
    return jsonify(data)

@api_rutas.route('/registrar', methods=['POST'])
def registrar_transaccion_api():
    if not session.get("usuario_id"):
        return jsonify({"error": "Sesión no válida"}), 401

    data = request.get_json()
    cuenta_id = data.get("cuenta_id")
    categoria_id = data.get("categoria_id")
    monto = data.get("monto")
    descripcion = data.get("descripcion", "")

    current_app.transaccion_facade.registrar_transaccion(cuenta_id, categoria_id, descripcion, monto, fecha=None)

    cuenta = current_app.cuenta_bancaria_facade.obtener_cuenta_por_id(cuenta_id)

    return jsonify({
        "mensaje": "Transacción registrada",
        "nuevo_saldo": cuenta.saldo
    }), 201

@api_rutas.route('/datos_graficos', methods=['GET'])
@login_requerido_api
def obtener_datos_graficos_api():
    usuario_id = session.get("usuario_id")
    cuenta_id = request.args.get('cuenta_id', type=int)
    year = request.args.get('year', type=int)
    month = request.args.get('month', type=int)
    day = request.args.get('day', type=int)

    # Validación de cuenta
    if cuenta_id:
        cuenta = current_app.cuenta_bancaria_facade.obtener_cuenta_por_id(cuenta_id)
        if cuenta is None or cuenta.usuario_id != usuario_id:
            return jsonify({"error": "Cuenta no encontrada o no pertenece al usuario"}), 403

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
    else:
        datos_grafico = {'ingresos': 0, 'gastos': 0, 'balance_neto': 0}
        grafico_gastos_categoria = []
        grafico_ingresos_categoria = []

    return jsonify({
        "datos_grafico": datos_grafico,
        "datos_grafico_categoria": grafico_gastos_categoria,
        "datos_grafico_categoria_ingreso": grafico_ingresos_categoria,
    })
