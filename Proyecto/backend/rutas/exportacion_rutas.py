from flask import Blueprint, session, request, current_app, send_file, jsonify
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import tempfile

exportacion_rutas = Blueprint('exportacion_rutas', __name__, url_prefix='/api/exportacion')

@exportacion_rutas.route('/exportar_excel', methods=['GET'])
def exportar_excel():
    """
    summary: Exporta los datos de la cuenta a un archivo Excel.
    description: Permite descargar un archivo Excel con los movimientos de la cuenta seleccionada del usuario autenticado.
    parameters:
      - in: query
        name: cuenta_id
        type: integer
        required: true
        description: ID de la cuenta bancaria a exportar.
    responses:
      200:
        description: Archivo Excel generado exitosamente.
        schema:
          type: string
          format: binary
      401:
        description: No autenticado.
      400:
        description: Se requiere el ID de la cuenta.
      500:
        description: Error interno al exportar.
    """
    usuario_id = session.get('usuario_id')
    cuenta_id = request.args.get('cuenta_id', type=int)
    if not usuario_id:
        return jsonify({'success': False, 'error': 'No autenticado.'}), 401
    if not cuenta_id:
        return jsonify({'success': False, 'error': 'Se requiere el ID de la cuenta.'}), 400
    try:
        output, usuario_nombre, nombre_cuenta = current_app.exportacion_facade.exportar_excel(usuario_id, cuenta_id)
        fecha_str = datetime.now().strftime('%Y%m%d_%H%M%S')
        nombre_archivo = f'reporte_{usuario_nombre}_{nombre_cuenta}_{fecha_str}.xlsx'
        response = send_file(
            output,
            as_attachment=True,
            download_name=nombre_archivo,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        return response
    except Exception as e:
        return jsonify({'success': False, 'error': f'Error: {str(e)}'}), 500

@exportacion_rutas.route('/importar_excel', methods=['POST'])
def importar_excel():
    """
    summary: Importa datos desde un archivo Excel.
    description: Permite importar movimientos a una cuenta bancaria desde un archivo Excel.
    parameters:
      - in: formData
        name: archivo_excel
        type: file
        required: true
        description: Archivo Excel a importar.
      - in: formData
        name: cuenta_id
        type: integer
        required: true
        description: ID de la cuenta bancaria.
    responses:
      200:
        description: Importación realizada correctamente.
        schema:
          type: object
          properties:
            success: {type: boolean}
            importadas: {type: integer}
            errores:
              type: array
              items: {type: string}
      400:
        description: Datos faltantes o inválidos.
      500:
        description: Error interno al importar.
    """
    archivo = request.files.get('archivo_excel')
    cuenta_id = request.form.get('cuenta_id')
    usuario_id = session.get('usuario_id')

    if not archivo or not cuenta_id or not usuario_id:
        return jsonify({"success": False, "importadas": 0, "errores": ["Faltan datos requeridos."]}), 400

    try:
        cuenta_id = int(cuenta_id)
        usuario_id = int(usuario_id)
    except (ValueError, TypeError):
        return jsonify({"success": False, "importadas": 0, "errores": ["ID de cuenta o usuario inválido."]}), 400

    filename = secure_filename(archivo.filename)
    with tempfile.NamedTemporaryFile(delete=False, suffix=filename) as tmp:
        archivo.save(tmp.name)
        ruta_temporal = tmp.name

    try:
        resultado = current_app.exportacion_facade.importar_excel(ruta_temporal, usuario_id, cuenta_id)
    finally:
        os.remove(ruta_temporal)

    resultado['success'] = resultado.get('ok', False)
    return jsonify(resultado)
