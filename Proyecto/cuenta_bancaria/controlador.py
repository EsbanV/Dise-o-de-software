from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, session
from cuenta_bancaria.servicio import CuentaBancariaServicio

def crear_cuenta_bancaria_controlador():
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
        return redirect(url_for('cuenta_rutas.gestionar_cuentas_bancarias'))
    return render_template('cuentas.html')

def obtener_cuentas_bancarias_controlador():
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        flash('Necesitas iniciar sesión para ver tus cuentas.', 'warning')
        return redirect(url_for('usuario_rutas.login'))
    
    cuentas = CuentaBancariaServicio.obtener_cuentas_bancarias(usuario_id)
    return render_template('cuentas.html', cuentas=cuentas)


def actualizar_cuenta_controlador(cuenta_id):
    cuenta = CuentaBancariaServicio.obtener_cuenta_por_id(cuenta_id)
    if not cuenta:
        flash('Cuenta no encontrada.', 'danger')
        return redirect(url_for('cuenta_rutas.gestionar_cuentas_bancarias'))
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        try:
            saldo = float(request.form.get('saldo'))
        except (TypeError, ValueError):
            saldo = cuenta.saldo
        CuentaBancariaServicio.actualizar_cuenta_bancaria(cuenta_id, nombre, saldo)
        flash('Cuenta actualizada exitosamente.', 'success')
        return redirect(url_for('cuenta_rutas.gestionar_cuentas_bancarias'))
    
    return render_template('cuenta_actualizar.html', cuenta=cuenta)

def eliminar_cuenta_bancaria_controlador(cuenta_id):
    CuentaBancariaServicio.eliminar_cuenta_bancaria(cuenta_id)
    flash('Cuenta eliminada.', 'success')
    return redirect(url_for('cuenta_rutas.gestionar_cuentas_bancarias'))

def resumen_cuenta_bancaria_controlador(cuenta_id):
    cuenta = CuentaBancariaServicio.obtener_cuenta_por_id(cuenta_id)
    if not cuenta:
        flash('Cuenta no encontrada.', 'danger')
        return redirect(url_for('cuenta_rutas.gestionar_cuentas_bancarias'))
    
    # Aquí puedes agregar lógica para calcular el resumen de la cuenta
    # Por ejemplo, obtener transacciones, saldo actual, etc.
    
    return render_template('resumen_cuenta.html', cuenta=cuenta)