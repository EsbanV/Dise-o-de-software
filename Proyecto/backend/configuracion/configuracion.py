from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from modelos import *
from configuracion.extensiones import db
from dotenv import load_dotenv
import os

# Carga automática del archivo .env
load_dotenv()

def crear_app():
    # Calcula la ruta base del proyecto (para carpetas static y templates)
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    app = Flask(
        __name__,
        static_folder=os.path.join(base_dir, 'static'),
        template_folder=os.path.join(base_dir, 'templates')
    )

    # Configuración tomada desde variables del entorno
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

    # Inicializa la base de datos con la app
    db.init_app(app)

    # Crea todas las tablas si no existen
    with app.app_context():
        db.create_all()

    return app