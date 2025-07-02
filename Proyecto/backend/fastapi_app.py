from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from modelos.usuario import Usuario
from modelos.cuenta_bancaria import CuentaBancaria
from modelos.categoria import Categoria
from modelos.transaccion import Transaccion
from modelos.presupuesto import Presupuesto
from servicios.usuario_servicio import UsuarioServicio
from servicios.cuenta_bancaria_servicio import CuentaBancariaServicio
from servicios.categoria_servicio import CategoriaServicio
from servicios.transaccion_servicio import TransaccionServicio
from servicios.presupuesto_servicio import PresupuestoServicio
from servicios.transaccion_base_datos import TransaccionRepositorio
from servicios.base_datos import ServicioBaseDatos
from fastapi.middleware.cors import CORSMiddleware
from configuracion.configuracion import db
from app import create_app

flask_app = create_app()

repositorio = ServicioBaseDatos(db.session)
presupuesto_servicio = PresupuestoServicio(repositorio)
transaccion_repositorio = TransaccionRepositorio(db.session)
categoria_servicio = CategoriaServicio(repositorio, presupuesto_servicio)
cuenta_bancaria_servicio = CuentaBancariaServicio(repositorio, categoria_servicio)
transaccion_servicio = TransaccionServicio(transaccion_repositorio, categoria_servicio)
usuario_servicio = UsuarioServicio(
    repositorio, transaccion_repositorio, cuenta_bancaria_servicio, categoria_servicio, transaccion_servicio
)

app = FastAPI(title="API Demo Servicios Reales", description="CRUD de usuarios, cuentas, categorías, transacciones y presupuestos")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # O ["*"] para desarrollo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------- Modelos Pydantic -----------

class UsuarioIn(BaseModel):
    nombre: str
    correo: str
    contrasena: str

class UsuarioOut(BaseModel):
    id: int
    nombre: str
    activo: bool
    correo: Optional[str] = None

class CuentaBancariaIn(BaseModel):
    nombre: str
    saldo: float
    usuario_id: int

class CuentaBancariaOut(BaseModel):
    id: int
    nombre: str
    saldo: float
    usuario_id: int

class CategoriaIn(BaseModel):
    cuenta_id: int
    nombre: str
    tipo: str
    presupuesto: Optional[float] = None

class CategoriaOut(BaseModel):
    id: int
    nombre: str
    tipo: str
    cuenta_id: int
    presupuesto: Optional[float] = None

class PresupuestoIn(BaseModel):
    categoria_id: int
    monto_asignado: float

class PresupuestoOut(BaseModel):
    id: int
    monto_asignado: float
    monto_gastado: float
    categoria_id: int

class TransaccionIn(BaseModel):
    monto: float
    descripcion: Optional[str] = ""
    categoria_id: int
    cuenta_bancaria_id: int

class TransaccionOut(BaseModel):
    id: int
    monto: float
    descripcion: Optional[str]
    fecha: Optional[datetime]
    categoria_id: int
    cuenta_bancaria_id: int

class GraficoTransaccionesOut(BaseModel):
    total_ingresos: float
    total_egresos: float
    cantidad_ingresos: int
    cantidad_egresos: int

class ListaMontosTransaccionOut(BaseModel):
    ingresos: List[float]
    egresos: List[float]


# ----------- Endpoints Usuarios -----------

@app.post("/api/usuarios/", response_model=UsuarioOut)
def crear_usuario(datos: UsuarioIn):
    with flask_app.app_context():
        try:
            usuario = usuario_servicio.registrar_usuario(datos.nombre, datos.correo, datos.contrasena)
            return UsuarioOut(
                id=usuario.id,
                nombre=usuario.nombre,
                correo=getattr(usuario, "correo", None),
                activo=getattr(usuario, "activo", True)
            )
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/usuarios/", response_model=List[UsuarioOut])
def listar_usuarios():
    with flask_app.app_context():
        try:
            usuarios = usuario_servicio.obtener_todos(Usuario)
            return [
                UsuarioOut(
                    id=u.id,
                    nombre=u.nombre,
                    correo=getattr(u, "correo", None),
                    activo=getattr(u, "activo", True)
                ) for u in usuarios
            ]
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

# ----------- Endpoints CuentaBancarias -----------

@app.post("/api/cuentas/", response_model=CuentaBancariaOut)
def crear_cuenta(datos: CuentaBancariaIn):
    with flask_app.app_context():
        try:
            cuenta = cuenta_bancaria_servicio.crear_cuenta(datos.nombre, datos.saldo, datos.usuario_id)
            return CuentaBancariaOut(
                id=cuenta.id,
                nombre=cuenta.nombre,
                saldo=cuenta.saldo,
                usuario_id=cuenta.usuario_id
            )
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/cuentas/", response_model=List[CuentaBancariaOut])
def listar_cuentas():
    with flask_app.app_context():
        try:
            cuentas = cuenta_bancaria_servicio.obtener_todos(CuentaBancaria)
            return [
                CuentaBancariaOut(
                    id=c.id,
                    nombre=c.nombre,
                    saldo=c.saldo,
                    usuario_id=c.usuario_id
                ) for c in cuentas
            ]
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

# ----------- Endpoints Categorías -----------

@app.post("/api/categorias/", response_model=CategoriaOut)
def crear_categoria(datos: CategoriaIn):
    with flask_app.app_context():
        try:
            categoria = categoria_servicio.crear_categoria(datos.cuenta_id, datos.nombre, datos.tipo, datos.presupuesto)
            monto_presupuesto = getattr(getattr(categoria, "presupuesto", None), "monto_asignado", None)
            return CategoriaOut(
                id=categoria.id,
                nombre=categoria.nombre,
                tipo=categoria.tipo,
                cuenta_id=categoria.cuenta_id,
                presupuesto=monto_presupuesto
            )
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/categorias/", response_model=List[CategoriaOut])
def listar_categorias():
    with flask_app.app_context():
        try:
            categorias = categoria_servicio.obtener_todos(Categoria)
            return [
                CategoriaOut(
                    id=cat.id,
                    nombre=cat.nombre,
                    tipo=cat.tipo,
                    cuenta_id=cat.cuenta_id,
                    presupuesto=getattr(getattr(cat, "presupuesto", None), "monto_asignado", None)
                ) for cat in categorias
            ]
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

# ----------- Endpoints Transacciones -----------

@app.post("/api/transacciones/", response_model=TransaccionOut)
def crear_transaccion(datos: TransaccionIn):
    with flask_app.app_context():
        try:
            transaccion = transaccion_servicio.registrar_transaccion(
                datos.cuenta_bancaria_id, datos.categoria_id, datos.descripcion, datos.monto, fecha=None
            )
            return TransaccionOut(
                id=transaccion.id,
                monto=transaccion.monto,
                descripcion=transaccion.descripcion,
                fecha=getattr(transaccion, "fecha", None),
                categoria_id=transaccion.categoria_id,
                cuenta_bancaria_id=transaccion.cuenta_bancaria_id
            )
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/transacciones/", response_model=List[TransaccionOut])
def listar_transacciones():
    with flask_app.app_context():
        try:
            transacciones = transaccion_servicio.obtener_todos(Transaccion)
            return [
                TransaccionOut(
                    id=t.id,
                    monto=t.monto,
                    descripcion=t.descripcion,
                    fecha=getattr(t, "fecha", None),
                    categoria_id=t.categoria_id,
                    cuenta_bancaria_id=t.cuenta_bancaria_id
                ) for t in transacciones
            ]
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
@app.get("/api/grafico/transacciones", response_model=GraficoTransaccionesOut)
def grafico_transacciones():
    with flask_app.app_context():
        try:
            transacciones = transaccion_servicio.obtener_todos(Transaccion)
            total_ingresos = sum(t.monto for t in transacciones if t.monto > 0)
            total_egresos = sum(abs(t.monto) for t in transacciones if t.monto < 0)
            cantidad_ingresos = len([t for t in transacciones if t.monto > 0])
            cantidad_egresos = len([t for t in transacciones if t.monto < 0])
            return GraficoTransaccionesOut(
                total_ingresos=total_ingresos,
                total_egresos=total_egresos,
                cantidad_ingresos=cantidad_ingresos,
                cantidad_egresos=cantidad_egresos
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
@app.get("/api/transacciones/montos", response_model=ListaMontosTransaccionOut)
def obtener_montos_transacciones():
    with flask_app.app_context():
        try:
            transacciones = transaccion_servicio.obtener_todos(Transaccion)
            ingresos = [t.monto for t in transacciones if t.monto > 0]
            egresos = [abs(t.monto) for t in transacciones if t.monto < 0]
            return ListaMontosTransaccionOut(
                ingresos=ingresos,
                egresos=egresos
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


# ----------- Endpoints Presupuestos -----------

@app.post("/api/presupuestos/", response_model=PresupuestoOut)
def crear_presupuesto(datos: PresupuestoIn):
    with flask_app.app_context():
        try:
            presupuesto = presupuesto_servicio.asignar_presupuesto(datos.categoria_id, datos.monto_asignado)
            return PresupuestoOut(
                id=presupuesto.id,
                monto_asignado=presupuesto.monto_asignado,
                monto_gastado=presupuesto.monto_gastado,
                categoria_id=presupuesto.categoria_id
            )
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/presupuestos/", response_model=List[PresupuestoOut])
def listar_presupuestos():
    with flask_app.app_context():
        try:
            presupuestos = presupuesto_servicio.obtener_todos(Presupuesto)
            return [
                PresupuestoOut(
                    id=p.id,
                    monto_asignado=p.monto_asignado,
                    monto_gastado=p.monto_gastado,
                    categoria_id=p.categoria_id
                ) for p in presupuestos
            ]
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
