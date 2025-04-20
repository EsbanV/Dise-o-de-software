# api_rutas.py
from flask import Blueprint, request, jsonify, session
from servicios.categoria_servicio import CategoriaServicio
from servicios.cuenta_bancaria_servicio import CuentaBancariaServicio
from servicios.transaccion_servicio import TransaccionServicio

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

        nueva_categoria = CategoriaServicio.crear_categoria(nombre, tipo, presupuesto, cuenta_id)
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

    cuenta = CuentaBancariaServicio.crear_cuenta(nombre, saldo_inicial, usuario_id)
    return jsonify({
        "mensaje": "Cuenta creada correctamente",
        "cuenta": {
            "id": cuenta.id,
            "nombre": cuenta.nombre,
            "saldo": cuenta.saldo
        }
    }), 201

@api_rutas.route('/categorias', methods=['GET'])
@login_requerido_api  # <-- si ya lo tienes
def obtener_categorias():
    cuenta_id = request.args.get('cuenta_id', type=int)
    tipo = request.args.get('tipo')

    print("✅ Entrando a /api/categorias con cuenta:", cuenta_id, "tipo:", tipo)

    if not cuenta_id:
        print("❌ Falta cuenta_id")
        return jsonify({"error": "Falta el ID de la cuenta"}), 400

    categorias = CategoriaServicio.obtener_categorias_filtradas(cuenta_id, tipo)

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

    transaccion = TransaccionServicio.registrar_transaccion(cuenta_id, categoria_id, descripcion, monto)

    # ✅ Obtener la cuenta bancaria después de registrar
    cuenta = CuentaBancariaServicio.obtener_cuenta_por_id(cuenta_id)

    return jsonify({
        "mensaje": "Transacción registrada",
        "nuevo_saldo": cuenta.saldo  # Ahora sí está definido
    }), 201
