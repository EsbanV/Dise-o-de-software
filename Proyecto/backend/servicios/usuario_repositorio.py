from servicios.base_datos import ServicioBaseDatos
from modelos.usuario import Usuario

class UsuarioRepositorio(ServicioBaseDatos):
    # Métodos CRUD simples ya heredados

    # Agrega métodos personalizados aquí si algún día necesitas
    def obtener_usuarios_activos(self, year=None, month=None, day=None):
        query = self.session.query(Usuario).filter(Usuario.activo == True)
        # Puedes agregar más lógica específica aquí si quieres filtrar por fecha de creación, etc.
        return query.all()
