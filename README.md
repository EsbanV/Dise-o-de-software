# Dise-o-de-software
proyecto de gestión y manejo de presupuesto

Patrones de Diseño para el Gestor de Presupuestos
1. Patrón Repositorio (Repository Pattern)
En qué consiste: Crea una capa de abstracción entre la lógica de negocio y la capa de acceso a datos. Proporciona una API unificada para interactuar con la fuente de datos, ocultando los detalles de implementación.
Por qué y para qué: Este patrón será fundamental en el proyecto para:

Abstraer la lógica de acceso a datos (SQLite) del resto de la aplicación
Permitir cambiar la implementación de la base de datos sin afectar otras partes del código
Facilitar pruebas unitarias mediante repositorios simulados (mocks)
Centralizar operaciones CRUD para cada entidad (Usuario, Cuenta, Categoría, etc.)

2. Patrón Servicio (Service Pattern)
En qué consiste: Encapsula la lógica de negocio en clases de servicio, separando las reglas de negocio de otras capas de la aplicación.
Por qué y para qué: Implementar este patrón nos ayudará a:

Mantener la lógica de presupuestos, transacciones y cálculos financieros separada de la interfaz
Proporcionar métodos reutilizables que coordinen múltiples operaciones
Centralizar validaciones de negocio complejas
Implementar transacciones que involucren múltiples entidades (ej: registrar una transacción y actualizar el saldo del presupuesto)

3. Patrón MVC (Model-View-Controller)
En qué consiste: Separa la aplicación en tres componentes: Modelo (datos), Vista (interfaz de usuario) y Controlador (lógica de control y comunicación).
Por qué y para qué: Este patrón es esencial para:

Organizar la estructura del proyecto Flask
Separar claramente la lógica de presentación (templates) de la lógica de negocio
Facilitar el mantenimiento y la escalabilidad
Permitir que diferentes desarrolladores trabajen en componentes distintos (frontend/backend)

4. Patrón Singleton
En qué consiste: Garantiza que una clase tenga una única instancia y proporciona un punto de acceso global a ella.
Por qué y para qué: Lo utilizaremos para:

Gestionar la conexión a la base de datos, asegurando una única instancia
Optimizar el uso de recursos al compartir conexiones
Mantener un estado consistente de la aplicación
Proporcionar acceso a servicios centralizados (como logging o configuración)

5. Patrón Strategy
En qué consiste: Define una familia de algoritmos, encapsula cada uno y los hace intercambiables. Permite que el algoritmo varíe independientemente de los clientes que lo utilizan.
Por qué y para qué: Este patrón será útil para:

Implementar diferentes estrategias de hashing de contraseñas
Permitir cambiar algoritmos de cálculo financiero (por ejemplo, diferentes formas de calcular estadísticas)
Implementar métodos flexibles de validación de datos
Facilitar la extensión de funcionalidades sin modificar código existente

6. Patrón Factory Method
En qué consiste: Define una interfaz para crear objetos, pero permite a las subclases decidir qué clase instanciar. Permite que una clase delegue la responsabilidad de instanciación a subclases.
Por qué y para qué: Lo aplicaremos para:

Crear instancias de repositorios o servicios según la configuración
Permitir extensiones futuras con diferentes implementaciones
Centralizar la lógica de creación de objetos complejos
Configurar la aplicación Flask con diferentes entornos (desarrollo, pruebas, producción)

7. Patrón DTO (Data Transfer Object)
En qué consiste: Crea objetos simples para transferir datos entre subsistemas, reduciendo llamadas remotas.
Por qué y para qué: Este patrón nos ayudará a:

Separar los modelos de base de datos de las estructuras usadas en la API
Controlar qué datos se transfieren entre capas
Simplificar las respuestas JSON de la API
Evitar la exposición de datos sensibles o innecesarios

8. Patrón Decorador
En qué consiste: Adjunta responsabilidades adicionales a un objeto dinámicamente, proporcionando una alternativa flexible a la herencia para extender funcionalidades.
Por qué y para qué: Lo implementaremos para:

Crear middlewares para verificar autenticación
Aplicar validaciones previas a ciertas operaciones
Implementar logging automático en operaciones críticas
Extender funcionalidades sin afectar clases existentes


Requerimientos para la Aplicación de Gestión de Presupuestos
Requerimientos Funcionales
Gestión de Usuarios

Registro de nuevos usuarios con nombre, correo electrónico y contraseña
Inicio de sesión con correo y contraseña
Recuperación de contraseña
Visualización y edición de perfil de usuario
Cierre de sesión

Gestión de Cuentas Bancarias

Creación de cuentas bancarias asociadas al usuario
Listado de cuentas bancarias del usuario
Modificación de información de cuentas bancarias
Eliminación de cuentas bancarias

Gestión de Categorías

Creación de categorías de gastos asociadas a cuentas bancarias
Listado de categorías por cuenta bancaria
Modificación de información de categorías
Eliminación de categorías

Gestión de Presupuestos

Asignación de presupuestos mensuales a categorías
Visualización de presupuestos por categoría
Actualización de montos de presupuestos
Visualización del saldo restante por presupuesto

Gestión de Transacciones

Registro de transacciones asociadas a una categoría
Visualización de historial de transacciones
Listado de transacciones por categoría o cuenta
Actualización automática del saldo restante al registrar transacciones

Gestión de Contenido

Visualización de artículos informativos
Creación de nuevos artículos (opcional para administradores)

Requerimientos No Funcionales
Seguridad

Almacenamiento seguro de contraseñas mediante hash y salt
Protección contra inyección SQL
Implementación de tokens de seguridad para sesiones
Validación de formularios en cliente y servidor
Protección contra CSRF (Cross-Site Request Forgery)

Usabilidad

Interfaz intuitiva y fácil de usar
Tiempo de respuesta menor a 2 segundos para operaciones estándar
Diseño responsivo que se adapte a diferentes dispositivos
Mensajes de error claros y específicos
Guías de usuario accesibles

Rendimiento

Capacidad para manejar al menos 1000 usuarios concurrentes
Optimización de consultas a la base de datos
Tiempo de carga inicial menor a 3 segundos

Mantenibilidad

Código modular siguiendo principios SOLID
Documentación completa del código
Logs de errores y actividades importantes
Estructura clara de directorios y componentes

Escalabilidad

Arquitectura que permita escalar horizontalmente
Independencia entre capas de presentación, lógica y datos

Compatibilidad

Funcionamiento correcto en navegadores modernos (Chrome, Firefox, Safari, Edge)
Compatibilidad con diferentes sistemas operativos

Producto Mínimo Viable (MVP)
Funcionalidades Esenciales

Registro e inicio de sesión:

Crear cuenta
Iniciar sesión
Cerrar sesión


Gestión básica de finanzas:

Crear cuenta bancaria
Crear categorías de gastos
Asignar presupuestos mensuales a categorías
Registrar transacciones
Visualizar saldo restante por categoría


Visualización de datos:

Listado de cuentas
Listado de categorías
Listado de transacciones
Resumen de presupuestos



Características de Calidad Mínimas

Seguridad básica:

Contraseñas hasheadas
Protección de rutas mediante sesiones
Validaciones básicas de formularios


Interfaz:

Diseño limpio y funcional
Navegación intuitiva
Adaptabilidad a móviles y escritorio


Base tecnológica:

Implementación POO completa
Separación de responsabilidades (MVC)
Gestión eficiente de la base de datos



Criterios de Aceptación del MVP

Un usuario puede registrarse, iniciar sesión y gestionar su perfil
Un usuario puede crear y gestionar cuentas bancarias, categorías y presupuestos
Un usuario puede registrar transacciones y ver cómo afectan a sus presupuestos
La aplicación proporciona feedback claro sobre las acciones del usuario
La aplicación mantiene la consistencia de los datos financieros
La interfaz es accesible en dispositivos móviles y de escritorio
El sistema responde en tiempos aceptables (<3 segundos)

Elementos Fuera del Alcance del MVP
Gráficos y visualizaciones avanzadas
Importación/exportación de datos
Notificaciones y alertas
Gestión de metas de ahorro
Integración con APIs bancarias reales
Funciones colaborativas o familiares
Aplicación móvil nativa