from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app

usuario_rutas = Blueprint('usuario_rutas', __name__, template_folder='../templates')

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
            current_app.usuario_facade.registrar_usuario(nombre, correo, password)
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
        
        try:
            usuario = current_app.usuario_facade.iniciar_sesion(correo, password)
        
            if usuario:
                session['usuario_id'] = usuario.id
                session['nombre'] = usuario.nombre
                session['logged_in'] = True
                flash('Inicio de sesión exitoso.', 'success')
                return redirect(url_for('index_rutas.home'))
            else:
                flash('Credenciales inválidas. Intenta nuevamente.', 'danger')
        except Exception as e:
            current_app.logger.error("Error al iniciar sesión: %s", e)
            flash(f'Error al iniciar sesión: {str(e)}', 'danger')
    
    return render_template('login.html')

@usuario_rutas.route('/logout')
def logout():
    session.pop('usuario_id', None)
    flash('Has cerrado sesión exitosamente.', 'success')
    return redirect(url_for('usuario_rutas.login'))

@usuario_rutas.route('/acerca_de')
def acerca_de():
    return render_template('acerca_de.html')
