from flask import Blueprint, render_template

index_rutas = Blueprint('index_rutas', __name__, template_folder='../templates')

@index_rutas.route('/')
def home():
    return render_template('index.html')
