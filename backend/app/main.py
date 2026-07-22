from fastapi import FastAPI
import app.models
from app.database import Base, engine
from app.routers.categoria import (
    router as categoria_router,
)

#Crea las tablas si todavía no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Pizzería",
    description="Backend para la gestión de productos, pedidos y ventas",
    version="1.0.0",
)

app.include_router(categoria_router)


@app.get("/")
def obtener_inicio():
    return {
        "estado": "correcto",
        "mensaje": "La API de la pizzería está funcionando",
    }


@app.get("/salud")
def verificar_salud():
    return {
        "servicio": "backend",
        "activo": True,
    }
