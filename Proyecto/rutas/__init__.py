import os
import importlib
from .usuario_rutas import usuario_bp
from .presupuesto_rutas import presupuesto_bp
from .transaccion_rutas import transaccion_bp


ruta_actual = os.path.dirname(__file__)
modulos = [f[:-3] for f in os.listdir(ruta_actual) if f.endswith("_rutas.py")]

for modulo in modulos:
    importlib.import_module(f".{modulo}", package="rutas")
