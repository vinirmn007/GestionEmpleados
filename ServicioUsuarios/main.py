from fastapi import FastAPI
from database import Base, engine
from routes.usuario_router import router as usuario_router

app = FastAPI(title="Servicio Usuarios")

@app.get("/")
def read_root():
    return {"mensaje": "¡Hola, Servicio Usuarios está funcionando!"}

app.include_router(usuario_router)
Base.metadata.create_all(bind=engine)