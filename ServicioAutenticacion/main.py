from fastapi import FastAPI

app = FastAPI(title="Servicio Autenticacion", version="1.0.0")

@app.get("/")
def read_root():
    return {"mensaje": "¡Hola, Servicio Autenticacion está funcionando!"}
