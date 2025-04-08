from flask import Blueprint, render_template, session
from flask import redirect, url_for, request, flash

index_rutas = Blueprint('index_rutas', __name__, template_folder='../templates')

@index_rutas.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('registro.html')
    return render_template('index.html')
