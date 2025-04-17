from flask.views import MethodView
from flask import render_template, request, redirect, url_for, flash, session

from categoria.controlador import (
    obtener_categorias_controlador,
    crear_categoria_controlador,
    actualizar_categoria_controlador,
    eliminar_categoria_controlador
)

class VistaCategorias(MethodView):
    def get(self):
        return obtener_categorias_controlador()
    def post(self):
        crear_categoria_controlador()
        return redirect(url_for('categoria_rutas.vista_categorias'))

class VistaCategoriaDetalle(MethodView):
    def get(self, categoria_id):
        return actualizar_categoria_controlador(categoria_id)
    def post(self, categoria_id):
        actualizar_categoria_controlador(categoria_id)
        return redirect(url_for('categoria_rutas.vista_categorias'))

class VistaCategoriaEliminar(MethodView):
    def post(self, categoria_id):
        return eliminar_categoria_controlador(categoria_id)
