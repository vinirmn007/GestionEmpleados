from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx

from models.models import *
from controller import create_access_token

app = FastAPI(title="Servicio Autenticacion", version="1.0.0")

# --- Configurar CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ajusta según necesidad
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#USER_SERVICE_URL = "http://servicio-usuarios:9001"
USER_SERVICE_URL = "http://127.0.0.1:9001"

@app.get("/auth")
def read_root():
    return {"mensaje": "¡Hola, Servicio Autenticacion está funcionando!"}


@app.post("/auth/login", response_model=Token, tags=["Autenticacion"])
async def login(data: LoginRequest):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{USER_SERVICE_URL}/usuarios/validate",
                json={"email": data.email, "password": data.password}
            )

            if response.status_code in (401, 404):
                raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos")
            response.raise_for_status()

        except httpx.RequestError as exc:
            raise HTTPException(status_code=503, detail=f"Servicio de usuarios inválido: {exc}")
        
    user_data = response.json()

    access_token = create_access_token({
        "sub": user_data["id"],
        "roles": user_data["rol"]
    })

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@app.post("/auth/logout")
def logout():
    return {"mensaje": "¡Adiós desde el Servicio Autenticacion!"}
