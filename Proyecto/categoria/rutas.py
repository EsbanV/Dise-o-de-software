from categoria.vistas import VistaCategorias, VistaCategoriaDetalle, VistaCategoriaEliminar
from flask import Blueprint

categoria = Blueprint('categorias', __name__)

categoria.add_url_rule(
    '/',
    view_func=VistaCategorias.as_view('vista_categorias'),
    methods=['GET', 'POST']
)
categoria.add_url_rule(
    '/actualizar/<int:categoria_id>',
    view_func=VistaCategoriaDetalle.as_view('detalle_categoria'),
    methods=['GET', 'POST']
)
categoria.add_url_rule(
    '/eliminar/<int:categoria_id>',
    view_func=VistaCategoriaEliminar.as_view('eliminar_categoria'),
    methods=['POST']
)