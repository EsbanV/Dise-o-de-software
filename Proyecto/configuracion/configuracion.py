from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from modelos import *
from extensiones import db

def crear_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///base_datos.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "AfkA?_X-Y198"

    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app
