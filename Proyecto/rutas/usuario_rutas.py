from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from servicios.autenticacion import ServicioAutenticacion
from servicios.usuario_servicio import UsuarioServicio

usuario_rutas = Blueprint('usuario_rutas', __name__, template_folder='../templates', static_folder='../static')

@usuario_rutas.route('/registro', methods=['GET', 'POST'])
def registrar_usuario():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        correo = request.form.get('correo')
        password = request.form.get('password')
        
        if not nombre or not correo or not password:
            flash('Todos los campos son requeridos.', 'warning')
            return render_template('registro.html')
        
        try:
            ServicioAutenticacion.registrar_usuario(nombre, correo, password)
            flash('Usuario registrado exitosamente.', 'success')
            return redirect(url_for('usuario_rutas.login'))
        except Exception as e:
            current_app.logger.error("Error al registrar usuario: %s", e)
            flash(f'Error al registrar el usuario: {str(e)}', 'danger')
    
    return render_template('registro.html')

@usuario_rutas.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form.get('correo')
        password = request.form.get('password')
        
        usuario = ServicioAutenticacion.autenticar_usuario(correo, password)
        if usuario:
            session['usuario_id'] = usuario.id
            session['logged_in'] = True
            flash('Inicio de sesión exitoso.', 'success')
            return redirect(url_for('index_rutas.home'))
        else:
            flash('Credenciales inválidas. Intenta nuevamente.', 'danger')
    
    return render_template('login.html')

@usuario_rutas.route('/logout')
def logout():
    session.pop('usuario_id', None)
    flash('Has cerrado sesión exitosamente.', 'success')
    return redirect(url_for('usuario_rutas.login'))
