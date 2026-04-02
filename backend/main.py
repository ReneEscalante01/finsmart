from fastapi import FastAPI
from dotenv import load_dotenv
from src.models.usuario import Usuario
from src.models.rol import Rol
from src.routers.auth import router as auth_router
from src.routers.categoria import router as categorias_router
from src.routers.cuenta import router as cuentas_router
from src.routers.presupuesto import router as presupuestos_router
from src.routers.transaccion import router as transacciones_router
from src.routers.usuario import router as usuarios_router
from src.routers.rol import router as roles_router

load_dotenv()

app = FastAPI(title="FinSmart API", version = "1.0.0")

app.include_router(auth_router)
app.include_router(categorias_router)
app.include_router(cuentas_router)
app.include_router(presupuestos_router)
app.include_router(transacciones_router)
app.include_router(usuarios_router)
app.include_router(roles_router)

@app.get("/")
def root():
    return {"message": "FinSmart API running"}