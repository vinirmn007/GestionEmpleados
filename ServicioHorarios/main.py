from fastapi import FastAPI

app = FastAPI(title="Servicio Horarios")

@app.get("/")
def read_root():
    return {"mensaje": "¡Hola, Servicio Horarios está funcionando!"}
