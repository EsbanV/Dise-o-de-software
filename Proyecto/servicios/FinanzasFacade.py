from typing import Dict, List, Optional, Any, Union
import logging

from modelos.usuario import Usuario
from modelos.cuenta_bancaria import CuentaBancaria
from modelos.categoria import Categoria, TipoCategoria
from modelos.presupuesto import Presupuesto
from modelos.transaccion import Transaccion
from modelos.publicacion import Publicacion

from servicios.usuario_servicio import UsuarioServicio
from servicios.cuenta_bancaria_servicio import CuentaBancariaServicio
from servicios.categoria_servicio import CategoriaServicio
from servicios.presupuesto_servicio import PresupuestoServicio
from servicios.transaccion_servicio import TransaccionServicio
from servicios.grafico_servicio import GraficoServicio
from servicios.autor_servicio import AutorService
from servicios.publicacion_servicio import PublicacionService
from servicios.notificacion_servicio import NotificacionService


class FinanzasFacade:
    """
    Facade que proporciona una interfaz unificada al sistema de finanzas personales.
    Simplifica las interacciones con los múltiples servicios subyacentes.
    """

    def __init__(self):
        """Inicializa la fachada sin necesidad de configuración externa."""
        logging.info("Inicializando FinanzasFacade")

    # === GESTIÓN DE USUARIOS ===
    
    def registrar_usuario(self, nombre: str, correo: str, contrasena: str) -> Usuario:
        """Registra un nuevo usuario en el sistema."""
        logging.info(f"FinanzasFacade: Registrando usuario: {correo}")
        return UsuarioServicio.registrar_usuario(nombre, correo, contrasena)
    
    def iniciar_sesion(self, correo: str, contrasena: str) -> Usuario:
        """Inicia sesión de un usuario."""
        logging.info(f"FinanzasFacade: Iniciando sesión: {correo}")
        return UsuarioServicio.iniciar_sesion(correo, contrasena)
    
    def actualizar_perfil(self, usuario_id: int, nombre: str = None, 
                          correo: str = None, contrasena: str = None) -> Usuario:
        """Actualiza los datos del perfil de un usuario."""
        logging.info(f"FinanzasFacade: Actualizando usuario: {usuario_id}")
        return UsuarioServicio.actualizar_usuario(usuario_id, nombre, correo, contrasena)
    
    def eliminar_cuenta(self, usuario_id: int) -> bool:
        """Elimina (desactiva) la cuenta de un usuario."""
        logging.info(f"FinanzasFacade: Eliminando usuario: {usuario_id}")
        return UsuarioServicio.eliminar_usuario(usuario_id)

    # === GESTIÓN DE CUENTAS BANCARIAS ===
    
    def crear_cuenta_bancaria(self, nombre: str, saldo_inicial: float, 
                              usuario_id: int) -> CuentaBancaria:
        """Crea una nueva cuenta bancaria para el usuario."""
        logging.info(f"FinanzasFacade: Creando cuenta bancaria para usuario: {usuario_id}")
        return CuentaBancariaServicio.crear_cuenta(nombre, saldo_inicial, usuario_id)
    
    def obtener_cuentas_bancarias(self, usuario_id: int) -> List[CuentaBancaria]:
        """Obtiene todas las cuentas bancarias de un usuario."""
        logging.info(f"FinanzasFacade: Obteniendo cuentas del usuario: {usuario_id}")
        return CuentaBancariaServicio.obtener_cuentas(usuario_id)
    
    def actualizar_cuenta_bancaria(self, cuenta_id: int, nombre: str = None, 
                                  saldo: float = None) -> CuentaBancaria:
        """Actualiza los datos de una cuenta bancaria."""
        logging.info(f"FinanzasFacade: Actualizando cuenta bancaria: {cuenta_id}")
        return CuentaBancariaServicio.actualizar_cuenta(cuenta_id, nombre, saldo)
    
    def eliminar_cuenta_bancaria(self, cuenta_id: int) -> CuentaBancaria:
        """Elimina una cuenta bancaria."""
        logging.info(f"FinanzasFacade: Eliminando cuenta bancaria: {cuenta_id}")
        return CuentaBancariaServicio.eliminar_cuenta(cuenta_id)

    # === GESTIÓN DE CATEGORÍAS ===
    
    def crear_categoria(self, nombre: str, tipo: str, presupuesto: float = None, 
                        cuenta_id: int = None) -> Categoria:
        """Crea una nueva categoría para la cuenta específica."""
        logging.info(f"FinanzasFacade: Creando categoría {nombre} para cuenta: {cuenta_id}")
        return CategoriaServicio.crear_categoria(nombre, tipo, presupuesto, cuenta_id)
    
    def obtener_categorias(self, cuenta_id: int) -> List[Categoria]:
        """Obtiene todas las categorías de una cuenta."""
        logging.info(f"FinanzasFacade: Obteniendo categorías para cuenta: {cuenta_id}")
        return CategoriaServicio.obtener_categorias(cuenta_id)
    
    def obtener_categorias_por_tipo(self, cuenta_id: int, tipo: str) -> List[Categoria]:
        """Obtiene categorías filtradas por tipo (INGRESO/GASTO)."""
        logging.info(f"FinanzasFacade: Obteniendo categorías tipo {tipo} para cuenta: {cuenta_id}")
        return CategoriaServicio.obtener_categorias_filtradas(cuenta_id, tipo)
    
    def actualizar_categoria(self, categoria_id: int, nombre: str) -> Categoria:
        """Actualiza el nombre de una categoría."""
        logging.info(f"FinanzasFacade: Actualizando categoría: {categoria_id}")
        return CategoriaServicio.actualizar_categoria(categoria_id, nombre)
    
    def eliminar_categoria(self, categoria_id: int) -> bool:
        """Elimina una categoría."""
        logging.info(f"FinanzasFacade: Eliminando categoría: {categoria_id}")
        return CategoriaServicio.eliminar_categoria(categoria_id)

    # === GESTIÓN DE PRESUPUESTOS ===
    
    def asignar_presupuesto(self, categoria_id: int, monto: float) -> Presupuesto:
        """Asigna o actualiza un presupuesto para una categoría."""
        logging.info(f"FinanzasFacade: Asignando presupuesto {monto} a categoría: {categoria_id}")
        return PresupuestoServicio.asignar_presupuesto(categoria_id, monto)
    
    def obtener_presupuesto(self, categoria_id: int) -> Optional[Presupuesto]:
        """Obtiene el presupuesto de una categoría."""
        logging.info(f"FinanzasFacade: Obteniendo presupuesto para categoría: {categoria_id}")
        return PresupuestoServicio.obtener_presupuesto(categoria_id)
    
    def eliminar_presupuesto(self, presupuesto_id: int) -> Optional[Presupuesto]:
        """Elimina un presupuesto."""
        logging.info(f"FinanzasFacade: Eliminando presupuesto: {presupuesto_id}")
        return PresupuestoServicio.eliminar_presupuesto(presupuesto_id)

    # === GESTIÓN DE TRANSACCIONES ===
    
    def registrar_transaccion(self, cuenta_id: int, categoria_id: int, 
                              descripcion: str, monto: float) -> Transaccion:
        """Registra una nueva transacción."""
        logging.info(f"FinanzasFacade: Registrando transacción en cuenta {cuenta_id}")
        return TransaccionServicio.registrar_transaccion(cuenta_id, categoria_id, descripcion, monto)
    
    def obtener_transacciones_cuenta(self, cuenta_id: int) -> List[Transaccion]:
        """Obtiene todas las transacciones de una cuenta."""
        logging.info(f"FinanzasFacade: Obteniendo transacciones de cuenta: {cuenta_id}")
        return TransaccionServicio.obtener_transacciones_por_cuenta(cuenta_id)
    
    def obtener_transacciones_categoria(self, categoria_id: int) -> List[Transaccion]:
        """Obtiene todas las transacciones de una categoría."""
        logging.info(f"FinanzasFacade: Obteniendo transacciones de categoría: {categoria_id}")
        return TransaccionServicio.obtener_transacciones_por_categoria(categoria_id)
    
    def actualizar_transaccion(self, transaccion_id: int, nuevo_monto: float) -> Optional[Transaccion]:
        """Actualiza el monto de una transacción."""
        logging.info(f"FinanzasFacade: Actualizando transacción: {transaccion_id}")
        return TransaccionServicio.actualizar_transaccion(transaccion_id, nuevo_monto)
    
    def eliminar_transaccion(self, transaccion_id: int) -> Optional[Transaccion]:
        """Elimina una transacción."""
        logging.info(f"FinanzasFacade: Eliminando transacción: {transaccion_id}")
        return TransaccionServicio.eliminar_transaccion(transaccion_id)

    # === REPORTES Y ANÁLISIS ===
    
    def obtener_resumen_financiero(self, usuario_id: int, cuenta_id: int = None) -> Dict:
        """Obtiene un resumen completo de la situación financiera del usuario."""
        logging.info(f"FinanzasFacade: Generando resumen financiero para usuario: {usuario_id}")
        return UsuarioServicio.obtener_resumen(usuario_id, cuenta_id)
    
    def obtener_datos_grafico(self, cuenta_id: int) -> Dict:
        """Obtiene datos para gráficos de resumen financiero."""
        logging.info(f"FinanzasFacade: Generando datos para gráfico de cuenta: {cuenta_id}")
        return GraficoServicio.obtener_datos_crudos(cuenta_id)
    
    def obtener_distribucion_gastos(self, cuenta_id: int) -> List[Dict]:
        """Obtiene la distribución de gastos por categoría."""
        logging.info(f"FinanzasFacade: Generando distribución de gastos para cuenta: {cuenta_id}")
        return GraficoServicio.obtener_datos_categorias_gasto(cuenta_id)

    # === SOCIAL Y COMUNIDAD ===
    
    def suscribirse_autor(self, subscriber_id: int, autor_id: int) -> Any:
        """Suscribe a un usuario a un autor."""
        logging.info(f"FinanzasFacade: Suscribiendo usuario {subscriber_id} a autor {autor_id}")
        return AutorService.suscribir(subscriber_id, autor_id)
    
    def dejar_de_seguir_autor(self, subscriber_id: int, autor_id: int) -> None:
        """Cancela la suscripción a un autor."""
        logging.info(f"FinanzasFacade: Cancelando suscripción de usuario {subscriber_id} a autor {autor_id}")
        return AutorService.desuscribir(subscriber_id, autor_id)
    
    def crear_publicacion(self, usuario_id: int, titulo: str, contenido: str) -> Publicacion:
        """Crea una nueva publicación."""
        logging.info(f"FinanzasFacade: Creando publicación por usuario: {usuario_id}")
        return PublicacionService.crear_publicacion(usuario_id, titulo, contenido)
    
    def obtener_publicaciones(self) -> List[Publicacion]:
        """Obtiene todas las publicaciones."""
        logging.info("FinanzasFacade: Obteniendo todas las publicaciones")
        return PublicacionService.obtener_publicaciones()
    
    def agregar_comentario(self, publicacion_id: int, usuario_id: int, contenido: str) -> Any:
        """Agrega un comentario a una publicación."""
        logging.info(f"FinanzasFacade: Agregando comentario a publicación {publicacion_id}")
        return PublicacionService.agregar_comentario(publicacion_id, usuario_id, contenido)
    
    def obtener_notificaciones(self, usuario_id: int) -> List:
        """Obtiene las notificaciones de un usuario."""
        logging.info(f"FinanzasFacade: Obteniendo notificaciones para usuario: {usuario_id}")
        return NotificacionService.obtener_notificaciones(usuario_id)
    
    def marcar_notificacion_leida(self, notificacion_id: int) -> Any:
        """Marca una notificación como leída."""
        logging.info(f"FinanzasFacade: Marcando notificación como leída: {notificacion_id}")
        return NotificacionService.marcar_como_leida(notificacion_id)