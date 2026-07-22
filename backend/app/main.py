from fastapi import FastAPI

app = FastAPI(
    title="API de Pizzería",
    description="Backend para la gestión de productos, pedidos y ventas",
    version="1.0.0",
)


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

@app.get("/prueba")
def obtener_inicio():
    return {
        "estado": "prueba",
        "mensaje": "Prueba Sincronización GitHub",
    }