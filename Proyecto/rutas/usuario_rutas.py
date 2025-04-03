from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from servicios.usuario_servicio import UsuarioServicio

usuario_bp = Blueprint('usuario_bp', __name__, template_folder='../plantillas', static_folder='../estaticos')

@usuario_bp.route('/registro', methods=['GET', 'POST'])
def registrar_usuario():
    """
    Ruta para registrar nuevos usuarios.
    En GET: Muestra el formulario de registro.
    En POST: Procesa los datos enviados y registra al usuario.
    """
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        correo = request.form.get('correo')
        password = request.form.get('password')
        
        if not nombre or not correo or not password:
            flash('Todos los campos son requeridos.', 'warning')
            return render_template('registro.html')
        
        try:
            UsuarioServicio.registrar_usuario(nombre, correo, password)
            flash('Usuario registrado exitosamente.', 'success')
            return redirect(url_for('usuario_bp.login'))
        except Exception as e:
            flash(f'Error al registrar el usuario: {str(e)}', 'danger')
    
    return render_template('registro.html')


@usuario_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form.get('correo')
        password = request.form.get('password')
        
        usuario = UsuarioServicio.autenticar_usuario(correo, password)
        if usuario:
            session['usuario_id'] = usuario.id
            flash('Inicio de sesión exitoso.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Credenciales inválidas. Intenta nuevamente.', 'danger')
    
    return render_template('login.html')

@usuario_bp.route('/logout')
def logout():
    """
    Ruta para cerrar sesión.
    """
    session.pop('usuario_id', None)
    flash('Has cerrado sesión exitosamente.', 'success')
    return redirect(url_for('usuario_bp.login'))
