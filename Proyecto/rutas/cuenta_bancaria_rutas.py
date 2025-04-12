from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, session, current_app
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

@cuenta_rutas.route('/cuentas_vista', methods=['GET', 'POST'])
def crear_cuenta_vista():
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        flash('Necesitas iniciar sesión para ver tus cuentas.', 'warning')
        return redirect(url_for('usuario_rutas.login'))
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        try:
            saldo_inicial = float(request.form.get('saldo_inicial'))
        except (TypeError, ValueError):
            saldo_inicial = 0
        CuentaBancariaServicio.crear_cuenta(nombre, saldo_inicial, usuario_id)
        flash('Cuenta creada exitosamente.', 'success')
        return redirect(url_for('cuenta_rutas.crear_cuenta_vista'))
    
    cuentas = CuentaBancariaServicio.obtener_cuentas(usuario_id)
    return render_template('cuentas.html', cuentas=cuentas)