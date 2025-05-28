from flask import Blueprint, session, request, current_app, send_file, redirect, url_for, flash
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import tempfile

exportacion_rutas = Blueprint('exportacion_rutas', __name__)

@exportacion_rutas.route('/exportar_excel')
def exportar_excel():
    usuario_id = session.get('usuario_id')
    cuenta_id = request.args.get('cuenta_id', type=int)
    if not usuario_id:
        return redirect(url_for('usuario_rutas.login'))
    if not cuenta_id:
        return "Se requiere el ID de la cuenta", 400
    try:
                
        output, usuario_nombre, nombre_cuenta = current_app.exportacion_facade.exportar_excel(usuario_id, cuenta_id)
        fecha_str = datetime.now().strftime('%Y%m%d_%H%M%S')
        nombre_archivo = f'reporte_{usuario_nombre}_{nombre_cuenta}_{fecha_str}.xlsx'
        print("Nombre del archivo generado:", nombre_archivo)

        response = send_file(
            output,
            as_attachment=True,
            download_name=nombre_archivo,  # attachment_filename=... si usas Flask <2.0
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        print("Response headers:", response.headers)
        return response

    except Exception as e:
        return f"Error: {str(e)}", 500

@exportacion_rutas.route('/importar_excel', methods=['POST'])
def importar_excel():
    archivo = request.files.get('archivo_excel')
    cuenta_id = request.form.get('cuenta_id')
    usuario_id = session.get('usuario_id')

    # Validación de presencia
    if not archivo or not cuenta_id or not usuario_id:
        flash('Faltan datos requeridos.', 'error')
        return redirect(url_for('index_rutas.home'))  # Ajusta el endpoint de tu dashboard

    # Conversión explícita y control de errores
    try:
        cuenta_id = int(cuenta_id)
        usuario_id = int(usuario_id)
    except (ValueError, TypeError):
        flash('ID de cuenta o usuario inválido.', 'error')
        return redirect(url_for('index_rutas.home'))

    # Guardar archivo temporal
    filename = secure_filename(archivo.filename)
    with tempfile.NamedTemporaryFile(delete=False, suffix=filename) as tmp:
        archivo.save(tmp.name)
        ruta_temporal = tmp.name

    try:
        resultado = current_app.exportacion_facade.importar_excel(ruta_temporal, usuario_id, cuenta_id)
    finally:
        os.remove(ruta_temporal)

    if resultado["ok"]:
        flash(f'Importación exitosa: {resultado["importadas"]} registros.', 'success')
    else:
        # Junta errores en una sola cadena si hay muchos
        mensaje_error = ' '.join(resultado["errores"]) if resultado.get("errores") else 'Ocurrió un error inesperado.'
        flash(f'Errores en la importación: {mensaje_error}', 'error')
    return redirect(url_for('index_rutas.home'))