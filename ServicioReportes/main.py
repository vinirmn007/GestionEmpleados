from fastapi import FastAPI

app = FastAPI(title="Servicio Reporetes")

@app.get("/")
def read_root():
    return {"mensaje": "¡Hola, Servicio Reportes está funcionando!"}
