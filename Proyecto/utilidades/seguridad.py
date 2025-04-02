from werkzeug.security import generate_password_hash, check_password_hash

def encriptar_contrasena(contrasena):
    return generate_password_hash(contrasena)

def verificar_contrasena(contrasena, hash_guardado):
    return check_password_hash(hash_guardado, contrasena)
