from fastapi import FastAPI

app = FastAPI(title="Servicio Autenticacion", version="1.0.0")

@app.get("/")
def read_root():
    return {"mensaje": "¡Hola, Servicio Autenticacion está funcionando!"}

@app.post("auth/login")
def login(email: str, password: str):
    return {"mensaje": f"Intento de inicio de sesión para {email}"}

@app.post("auth/logout")
def logout():
    return {"mensaje": "¡Adiós desde el Servicio Autenticacion!"}

@app.post("auth/refresh")
def refresh_token():
    return {"mensaje": "Token de autenticación renovado"}
