import re

# valida que reciba un email
def validar_email(email):
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email) is not None

# valida que reciba una contraseña segura (8 caracteres, al menos una mayúscula, una minúscula, un número y un carácter especial)
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
