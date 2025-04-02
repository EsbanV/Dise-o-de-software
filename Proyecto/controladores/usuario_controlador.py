from flask import Blueprint, request, jsonify
from servicios.autenticacion import ServicioAutenticacion

usuario_bp = Blueprint("usuario_bp", __name__)

@usuario_bp.route("/registro", methods=["POST"])
def registrar_usuario():
    datos = request.json
    try:
        usuario = ServicioAutenticacion.registrar_usuario(
            datos["nombre"], datos["correo"], datos["contrasena"]
        )
        return jsonify({"mensaje": "Usuario registrado", "id": usuario.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@usuario_bp.route("/login", methods=["POST"])
def login():
    datos = request.json
    usuario = ServicioAutenticacion.autenticar_usuario(datos["correo"], datos["contrasena"])
    
    if usuario:
        return jsonify({"mensaje": "Inicio de sesión exitoso", "usuario_id": usuario.id})
    return jsonify({"error": "Credenciales inválidas"}), 401
