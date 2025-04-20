import re

def validar_email(email):
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email) is not None


def validar_password(password, min_length=8):
    if len(password) < min_length:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'\d', password):
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    return True

def validar_nombre(nombre, min_length=2):
    if not nombre or len(nombre.strip()) < min_length:
        return False
    if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', nombre):
        return False
    return True

def validar_datos_usuario(correo, contrasena):
    if not validar_nombre:
        raise ValueError("Nombre invalido")
    if not validar_email(correo):
        raise ValueError("Email inválido")
    if not validar_password(contrasena):
        raise ValueError("Contraseña inválida")

def validar_monto(monto):
    try:
        return float(monto) >= 0
    except (ValueError, TypeError):
        return False
