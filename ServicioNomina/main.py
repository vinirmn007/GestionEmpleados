from fastapi import FastAPI

app = FastAPI(title="Servicio Nomina")

@app.get("/")
def read_root():
    return {"mensaje": "¡Hola, Servicio Nomina está funcionando!"}

