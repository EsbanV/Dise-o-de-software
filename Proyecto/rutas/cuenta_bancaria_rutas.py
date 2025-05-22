from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, session, current_app

cuenta_rutas = Blueprint('cuenta_rutas', __name__)

@cuenta_rutas.route('/cuentas_vista', methods=['GET', 'POST'])
def gestionar_cuentas():
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
        current_app.cuenta_bancaria_servicio.crear_cuenta(nombre, saldo_inicial, usuario_id)
        flash('Cuenta creada exitosamente.', 'success')
        return redirect(url_for('cuenta_rutas.gestionar_cuentas'))

    cuentas = current_app.cuenta_bancaria_servicio.obtener_cuentas(usuario_id)
    return render_template('cuentas.html', cuentas=cuentas, cuenta=None, categorias=[])


@cuenta_rutas.route('/cuentas/actualizar/<int:cuenta_id>', methods=['GET', 'POST'])
def actualizar_cuenta_vista(cuenta_id):
    cuenta = current_app.cuenta_bancaria_servicio.obtener_cuenta_por_id(cuenta_id)
    if not cuenta:
        flash('Cuenta no encontrada.', 'danger')
        return redirect(url_for('cuenta_rutas.crear_cuenta_vista'))
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        try:
            saldo = float(request.form.get('saldo'))
        except (TypeError, ValueError):
            saldo = cuenta.saldo
        current_app.cuenta_bancaria_servicio.actualizar_cuenta(cuenta_id, nombre, saldo)
        flash('Cuenta actualizada exitosamente.', 'success')
        return redirect(url_for('cuenta_rutas.crear_cuenta_vista'))
    
    return render_template('cuenta_actualizar.html', cuenta=cuenta)

@cuenta_rutas.route('/cuentas/eliminar/<int:cuenta_id>', methods=['POST'])
def eliminar_cuenta_vista(cuenta_id):
    current_app.cuenta_bancaria_servicio.eliminar_cuenta(cuenta_id)
    flash('Cuenta eliminada.', 'success')
    return redirect(url_for('cuenta_rutas.gestionar_cuentas'))

@cuenta_rutas.route('/obtener/<int:cuenta_id>', methods=['GET'])
def datos_cuenta(cuenta_id):
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        flash('Necesitas iniciar sesión para ver tus cuentas.', 'warning')
        return redirect(url_for('usuario_rutas.login'))
    
    cuenta = current_app.cuenta_bancaria_servicio.obtener_cuenta_por_id(cuenta_id)
    if not cuenta:
        flash('Cuenta no encontrada.', 'danger')
        return redirect(url_for('cuenta_rutas.gestionar_cuentas'))

    categorias = current_app.categoria_servicio.obtener_categorias(cuenta_id)
    lista_categorias = [c for c in categorias]

    cuentas = current_app.cuenta_bancaria_servicio.obtener_cuentas(cuenta.usuario_id)
    return render_template('cuentas.html', cuentas=cuentas, cuenta=cuenta, categorias=lista_categorias)

@cuenta_rutas.route('/<int:cuenta_id>/categorias', methods=['GET'])
def obtener_categorias_por_cuenta(cuenta_id):
    categorias = current_app.categoria_servicio.obtener_categorias(cuenta_id)
    lista = [
        {"id": c.id, "nombre": c.nombre, "tipo": c.tipo}
        for c in categorias
    ]
    return jsonify(lista)
