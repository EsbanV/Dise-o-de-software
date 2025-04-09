from servicios.base_datos import ServicioBaseDatos
from servicios.usuario_servicio import UsuarioServicio
from servicios.categoria_servicio import CategoriaServicio
from servicios.transaccion_servicio import TransaccionServicio
from servicios.cuenta_bancaria_servicio import CuentaBancariaServicio
from servicios.presupuesto_servicio import  PresupuestoServicio


from utilidades.seguridad import encriptar_contrasena, verificar_contrasena

class ServicioAutenticacion:
    @staticmethod
    def registrar_usuario(nombre, correo, contrasena):
        contrasena_hash = encriptar_contrasena(contrasena)
        nuevo_usuario = UsuarioServicio.crear_usuario(nombre, correo, contrasena_hash)
        ServicioBaseDatos.agregar(nuevo_usuario)
        return nuevo_usuario

    @staticmethod
    def autenticar_usuario(correo, contrasena):
        usuario = UsuarioServicio.obtener_usuario_por_correo(correo)
        if usuario and verificar_contrasena(usuario.contrasena, contrasena):
            return usuario
        return None
    

