import os
import importlib
from .usuario_rutas import usuario_rutas
from .cuenta_bancaria_rutas import cuenta_rutas
from .categoria_rutas import categoria_rutas
from .presupuesto_rutas import presupuesto_rutas
from .transaccion_rutas import transaccion_rutas
from .index_rutas import index_rutas



ruta_actual = os.path.dirname(__file__)
modulos = [f[:-3] for f in os.listdir(ruta_actual) if f.endswith("_rutas.py")]

for modulo in modulos:
    importlib.import_module(f".{modulo}", package="rutas")
