from fastapi import FastAPI

app = FastAPI(title="Servicio Usuarios")

@app.get("/")
def read_root():
    return {"mensaje": "¡Hola, Servicio Usuarios está funcionando!"}
