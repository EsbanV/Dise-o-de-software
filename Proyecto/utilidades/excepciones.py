class ErrorNegocio(Exception):
    """Errores predecibles por reglas de negocio (status 400)."""
    def __init__(self, mensaje: str, codigo: str = None):
        self.codigo = codigo or "ERR_NEGOCIO"
        super().__init__(mensaje)

class ErrorTecnico(Exception):
    """Errores técnicos inesperados (status 500)."""
    def __init__(self, mensaje: str = None):
        mensaje = mensaje or "Error interno del sistema."
        super().__init__(mensaje)