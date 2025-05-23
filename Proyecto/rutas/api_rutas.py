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

    current_app.transaccion_facade.registrar_transaccion(cuenta_id, categoria_id, descripcion, monto)

    cuenta = current_app.cuenta_bancaria_facade.obtener_cuenta_por_id(cuenta_id)

    return jsonify({
        "mensaje": "Transacción registrada",
        "nuevo_saldo": cuenta.saldo
    }), 201

@api_rutas.route('/api/graficos', methods=['GET'])
@login_requerido_api
def obtener_datos_graficos_api():
    usuario_id = session.get("usuario_id")
    transacciones = current_app.grafico_facade.obtener_datos_crudos(usuario_id)

    ingresos, gastos = [], []
    gastos_cat, ingresos_cat, historico = {}, {}, {}

    for t in transacciones:
        tipo = t.categoria.tipo if t.categoria else 'DESCONOCIDO'
        monto = abs(t.monto)
        nombre_cat = t.categoria.nombre if t.categoria else 'Sin categoría'

        if tipo == 'INGRESO':
            ingresos.append(monto)
            ingresos_cat[nombre_cat] = ingresos_cat.get(nombre_cat, 0) + monto
        elif tipo == 'GASTO':
            gastos.append(monto)
            gastos_cat[nombre_cat] = gastos_cat.get(nombre_cat, 0) + monto

        if t.fecha >= datetime.now() - timedelta(days=30):
            dia = t.fecha.strftime('%Y-%m-%d')
            historico[dia] = historico.get(dia, 0) + t.monto

    return jsonify({
        "balance": [
            {"tipo": "INGRESOS", "total": sum(ingresos)},
            {"tipo": "GASTOS", "total": sum(gastos)}
        ],
        "gastos_categoria": [{"nombre": k, "total": v} for k, v in gastos_cat.items()],
        "ingresos_categoria": [{"nombre": k, "total": v} for k, v in ingresos_cat.items()],
        "historico": [{"dia": k, "total": v} for k, v in sorted(historico.items())],
        "totales": {
            "ingresos": sum(ingresos),
            "gastos": sum(gastos),
            "balance_neto": sum(ingresos) - sum(gastos)
        }
    })