from flask import Blueprint, request, jsonify
from servicios.transaccion_servicio import TransaccionServicio

transaccion_rutas = Blueprint('transaccion_rutas', __name__)

@transaccion_rutas.route('/transacciones', methods=['POST'])
def registrar_transaccion():
    data = request.get_json()
    categoria_id = data.get('categoria_id')
    monto = data.get('monto')
    try:
        transaccion = TransaccionServicio.registrar_transaccion(categoria_id, monto)
        return jsonify({
            "id": transaccion.id,
            "categoria_id": transaccion.categoria_id,
            "monto": transaccion.monto,
            "fecha": transaccion.fecha.isoformat()
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@transaccion_rutas.route('/transacciones/<int:categoria_id>', methods=['GET'])
def listar_transacciones(categoria_id):
    transacciones = TransaccionServicio.obtener_transacciones(categoria_id)
    transacciones_serializadas = [{
        "id": t.id,
        "monto": t.monto,
        "fecha": t.fecha.isoformat()
    } for t in transacciones]
    return jsonify(transacciones_serializadas), 200
