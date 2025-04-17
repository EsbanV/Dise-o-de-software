from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from configuracion.extensiones import db
import os

def crear_app():

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    app = Flask(__name__,static_folder=os.path.join(base_dir, 'static'),template_folder=os.path.join(base_dir, 'templates'))
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///base_datos.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "AfkA?_X-Y198"

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app
