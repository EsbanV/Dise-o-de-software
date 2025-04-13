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
    
    @staticmethod
    def registrar_banco(nombre, saldo_inicial, usuario_id):
        nueva_cuenta = CuentaBancariaServicio.crear_cuenta(nombre, saldo_inicial, usuario_id)
        ServicioBaseDatos.agregar(nueva_cuenta)
        cuenta_id = CuentaBancariaServicio.obtener_cuenta_por_id(nueva_cuenta.id)

        CategoriaServicio.crear_categoria("Gastos", cuenta_id)
        CategoriaServicio.crear_categoria("Ingresos", cuenta_id)
        CategoriaServicio.crear_categoria("Ahorros", cuenta_id)
        CategoriaServicio.crear_categoria("Inversiones", cuenta_id)
        CategoriaServicio.crear_categoria("Otros", cuenta_id)
        CategoriaServicio.crear_categoria("Comida", cuenta_id)
        CategoriaServicio.crear_categoria("Transporte", cuenta_id)
        CategoriaServicio.crear_categoria("Salud", cuenta_id)
        CategoriaServicio.crear_categoria("Entretenimiento", cuenta_id)
        CategoriaServicio.crear_categoria("Educación", cuenta_id)
        CategoriaServicio.crear_categoria("Ropa", cuenta_id)
        CategoriaServicio.crear_categoria("Hogar", cuenta_id)
        
        return nueva_cuenta
    

