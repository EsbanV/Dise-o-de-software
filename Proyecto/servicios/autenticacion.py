from repositorios.base_datos import BaseDatos
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
        BaseDatos.agregar(nuevo_usuario)
        return nuevo_usuario

    @staticmethod
    def autenticar_usuario(correo, contrasena):
        usuario = UsuarioServicio.obtener_usuario_por_correo(correo)
        if usuario and verificar_contrasena(usuario.contrasena, contrasena):
            return usuario
        return None
    
    @staticmethod
    def registrar_banco(nombre, saldo_inicial, usuario_id):
        nueva_cuenta = CuentaBancariaServicio.crear_cuenta(nombre, saldo_inicial, usuario_id)
        BaseDatos.agregar(nueva_cuenta)
        cuenta_id = CuentaBancariaServicio.obtener_cuenta_por_id(nueva_cuenta.id)

        default = ["Gastos", "Ingresos", "Ahorros", "Inversiones", "Otros", "Comida", "Transporte", "Salud", "Entretenimiento", "Educación", "Ropa", "Hogar"]
        for categoria in default:
            CategoriaServicio.crear_categoria(categoria, cuenta_id)
        
        return nueva_cuenta
    

