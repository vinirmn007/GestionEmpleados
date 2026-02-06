from fastapi import FastAPI

app = FastAPI(title="Servicio Notificaciones", version="1.0.0")

@app.get("/")
def read_root():
    return {"mensaje": "¡Hola, Servicio Notificaciones está funcionando!"}
