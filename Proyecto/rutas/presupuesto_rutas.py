from flask import Blueprint, request, jsonify
from servicios.presupuesto_servicio import PresupuestoServicio

presupuesto_rutas = Blueprint('presupuesto_rutas', __name__)

@presupuesto_rutas.route('/presupuestos', methods=['POST'])
def asignar_presupuesto():
    data = request.get_json()
    categoria_id = data.get('categoria_id')
    monto_asignado = data.get('monto_asignado')
    presupuesto = PresupuestoServicio.asignar_presupuesto(categoria_id, monto_asignado)
    return jsonify({
        "id": presupuesto.id,
        "categoria_id": presupuesto.categoria_id,
        "monto_asignado": presupuesto.monto_asignado,
        "monto_gastado": presupuesto.monto_gastado
    }), 201

@presupuesto_rutas.route('/presupuestos/<int:categoria_id>', methods=['GET'])
def obtener_presupuesto(categoria_id):
    presupuesto = PresupuestoServicio.obtener_presupuesto(categoria_id)
    if presupuesto:
        return jsonify({
            "id": presupuesto.id,
            "categoria_id": presupuesto.categoria_id,
            "monto_asignado": presupuesto.monto_asignado,
            "monto_gastado": presupuesto.monto_gastado
        }), 200
    else:
        return jsonify({"mensaje": "Presupuesto no encontrado"}), 404
