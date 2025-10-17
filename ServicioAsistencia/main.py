from fastapi import FastAPI

app = FastAPI(title="Servicio Asistencia", version="1.0.0")

@app.get("/")
def read_root():
    return {"mensaje": "¡Hola, Servicio Asistencia está funcionando!"}
