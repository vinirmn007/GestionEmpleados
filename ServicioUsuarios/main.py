from fastapi import FastAPI
from routes.usuario_router import router as usuario_router

app = FastAPI(title="Servicio Usuarios")

@app.get("/")
def read_root():
    return {"mensaje": "¡Hola, Servicio Usuarios está funcionando!"}

app.include_router(usuario_router)