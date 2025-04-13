from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, session
from servicios.presupuesto_servicio import PresupuestoServicio
from servicios.categoria_servicio import CategoriaServicio
from controladores.presupuesto_controlador import gestionar_presupuestos_controller, eliminar_presupuesto_controller

presupuesto_rutas = Blueprint('presupuesto_rutas', __name__)

@presupuesto_rutas.route('/presupuestos_vista', methods=['GET', 'POST'])
def gestionar_presupuestos():
    return gestionar_presupuestos_controller()

@presupuesto_rutas.route('/presupuestos/eliminar/<int:presupuesto_id>', methods=['POST'])
def eliminar_presupuesto_vista(presupuesto_id):
    return eliminar_presupuesto_controller(presupuesto_id)