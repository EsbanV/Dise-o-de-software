from flask import Blueprint, session, request, current_app, send_file, redirect, url_for
from datetime import datetime

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
