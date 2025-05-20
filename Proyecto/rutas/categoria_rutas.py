from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, session
from servicios.categoria_servicio import CategoriaServicio
from servicios.cuenta_bancaria_servicio import CuentaBancariaServicio

categoria_rutas = Blueprint('categoria_rutas', __name__)

@categoria_rutas.route('/categorias_vista', methods=['GET', 'POST'])
def crear_categoria_vista():

    if request.method == 'POST':
        try:
            cuenta_id = int(request.form.get('cuenta_id'))
            if not cuenta_id:
                flash("Debes seleccionar una cuenta para crear la categoría.", "danger")
                return redirect(url_for('cuenta_rutas.gestionar_cuentas'))
            nombre = request.form.get('nombre')
            tipo = request.form.get('tipo')
            presupuesto = request.form.get('presupuesto', '').strip()
            presupuesto = float(presupuesto) if presupuesto else None

            CategoriaServicio.crear_categoria(nombre, tipo, presupuesto, cuenta_id)
            flash('Categoría creada exitosamente.', 'success')
        except (TypeError, ValueError) as e:
            flash(f'Error al crear la categoría: {e}', 'danger')
            return redirect(url_for('categoria_rutas.crear_categoria_vista'))

    return redirect(url_for('cuenta_rutas.gestionar_cuentas'))


@categoria_rutas.route('/categorias', methods=['GET'])
def gestionar_categorias():
    usuario_id = session.get('usuario_id')
    if not usuario_id:
        flash("Inicia sesión para continuar.", "warning")
        return redirect(url_for("usuario_rutas.login"))

    cuenta_id = request.args.get('cuenta_id', type=int)
    tipo = request.args.get('tipo')

    cuentas = CuentaBancariaServicio.obtener_cuentas(usuario_id)

    categorias = CategoriaServicio.obtener_categorias_filtradas(cuenta_id, tipo)

    return render_template(
        "cuentas.html",
        cuentas=cuentas,
        categorias=categorias,
        cuenta_id=cuenta_id,
        tipo=tipo
    )

@categoria_rutas.route('/actualizar/<int:categoria_id>', methods=['GET', 'POST'])
def actualizar_categoria_vista(categoria_id):
    categoria = CategoriaServicio.obtener_categoria_por_id(categoria_id)
    if not categoria:
        flash('Categoría no encontrada.', 'danger')
        return redirect(url_for('categoria_rutas.gestionar_categorias'))
    
    if request.method == 'POST':
        nuevo_nombre = request.form.get('nombre')
        CategoriaServicio.actualizar_categoria(categoria_id, nuevo_nombre)
        flash('Categoría actualizada.', 'success')
        return redirect(url_for('categoria_rutas.gestionar_categorias'))
    
    return render_template('cuentas.html', categoria=categoria)



@categoria_rutas.route('/eliminar/<int:categoria_id>', methods=['POST'])
def eliminar_categoria_vista(categoria_id):
    CategoriaServicio.eliminar_categoria(categoria_id)
    flash('Categoría eliminada.', 'success')
    return redirect(url_for('categoria_rutas.gestionar_categorias'))


