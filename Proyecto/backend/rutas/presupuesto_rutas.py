from flask import Blueprint, request, jsonify, session, current_app

presupuesto_rutas = Blueprint('presupuesto_rutas', __name__)

@presupuesto_rutas.route('/', methods=['GET'])
def obtener_presupuestos():
    """
    summary: Obtiene los presupuestos asignados por categoría del usuario autenticado.
    description: Retorna todas las categorías y sus presupuestos asociados para el usuario autenticado.
    responses:
      200:
        description: Presupuestos obtenidos correctamente.
        schema:
          type: object
          properties:
            success: {type: boolean}
            categorias:
              type: array
              items:
                type: object
                properties:
                  id: {type: integer}
                  nombre: {type: string}
                  tipo: {type: string}
                  presupuesto: {type: number}
      401:
        description: Necesitas iniciar sesión.
    """
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return jsonify({'success': False, 'error': 'Necesitas iniciar sesión'}), 401
    try:
        categorias = current_app.categoria_facade.obtener_categorias_por_usuario(usuario_id)
        categorias_json = []
        for categoria in categorias:
            presupuesto = current_app.presupuesto_facade.obtener_presupuesto(categoria.id)
            categoria_dict = categoria.to_dict()
            categoria_dict['presupuesto'] = presupuesto
            categorias_json.append(categoria_dict)
        return jsonify({'success': True, 'categorias': categorias_json}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@presupuesto_rutas.route('/', methods=['POST'])
def asignar_presupuestos():
    """
    summary: Asigna o actualiza los presupuestos de las categorías del usuario autenticado.
    description: Recibe un diccionario con montos y los asigna a las categorías del usuario.
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          description: Diccionario con id de la categoría como clave y monto como valor.
    responses:
      200:
        description: Presupuestos actualizados correctamente.
        schema:
          type: object
          properties:
            success: {type: boolean}
            message: {type: string}
            actualizados:
              type: array
              items:
                type: object
                properties:
                  categoria_id: {type: integer}
                  monto: {type: number}
      400:
        description: Algunos montos son inválidos.
      401:
        description: Necesitas iniciar sesión.
    """
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return jsonify({'success': False, 'error': 'Necesitas iniciar sesión'}), 401
    try:
        categorias = current_app.categoria_facade.obtener_categorias_por_usuario(usuario_id)
        data = request.get_json()
        presupuestos_actualizados = []
        errores = []
        for categoria in categorias:
            monto = data.get(str(categoria.id)) or data.get(categoria.id)
            if monto is not None:
                try:
                    current_app.presupuesto_facade.asignar_presupuesto(categoria.id, float(monto))
                    presupuestos_actualizados.append({'categoria_id': categoria.id, 'monto': float(monto)})
                except ValueError:
                    errores.append({'categoria_id': categoria.id, 'error': 'Monto inválido'})
        if errores:
            return jsonify({'success': False, 'error': 'Algunos montos inválidos', 'errores': errores}), 400
        return jsonify({'success': True, 'message': 'Presupuestos actualizados correctamente.', 'actualizados': presupuestos_actualizados}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@presupuesto_rutas.route('/<int:presupuesto_id>/', methods=['DELETE'])
def eliminar_presupuesto(presupuesto_id):
    """
    summary: Elimina un presupuesto asignado a una categoría.
    description: Elimina el presupuesto de la categoría indicada por ID.
    parameters:
      - in: path
        name: presupuesto_id
        type: integer
        required: true
    responses:
      200:
        description: Presupuesto eliminado correctamente.
      401:
        description: Necesitas iniciar sesión.
      400:
        description: Error al eliminar el presupuesto.
    """
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        return jsonify({'success': False, 'error': 'Necesitas iniciar sesión'}), 401
    try:
        current_app.presupuesto_facade.eliminar_presupuesto(presupuesto_id)
        return jsonify({'success': True, 'message': 'Presupuesto eliminado.'}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400
