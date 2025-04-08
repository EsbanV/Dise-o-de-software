from flask import Blueprint, request, jsonify
from servicios.cuenta_bancaria_servicio import CuentaBancariaServicio

cuenta_rutas = Blueprint('cuenta_rutas', __name__)

@cuenta_rutas.route('/cuentas', methods=['POST'])
def crear_cuenta():
    data = request.get_json()
    nombre = data.get('nombre')
    saldo_inicial = data.get('saldo_inicial', 0)
    usuario_id = data.get('usuario_id')
    cuenta = CuentaBancariaServicio.crear_cuenta(nombre, saldo_inicial, usuario_id)
    return jsonify({"id": cuenta.id, "nombre": cuenta.nombre, "saldo": cuenta.saldo}), 201

@cuenta_rutas.route('/cuentas/<int:usuario_id>', methods=['GET'])
def listar_cuentas(usuario_id):
    cuentas = CuentaBancariaServicio.obtener_cuentas(usuario_id)
    cuentas_serializadas = [{"id": c.id, "nombre": c.nombre, "saldo": c.saldo} for c in cuentas]
    return jsonify(cuentas_serializadas), 200
