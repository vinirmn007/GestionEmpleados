from fastapi import FastAPI, Depends, HTTPException, status, Request
from datetime import timedelta
from fastapi.middleware.cors import CORSMiddleware
import httpx

from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException

from models.models import *
from secret_keys_settings import settings

app = FastAPI(title="Servicio Autenticacion", version="1.0.0")

@app.get("/auth")
def read_root():
    return {"mensaje": "¡Hola, Servicio Autenticacion está funcionando!"}

#carga config del .env
@AuthJWT.load_config
def get_config():
    return settings


#origenes permitidos
origins = [
    #"http://localhost:8080",
    "*"
]

#cinfigurar cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Para pruebas: USER_SERVICE_URL = "http://localhost:8000"
USER_SERVICE_URL = "http://servicio-usuarios:9001"

@app.post("/auth/login", response_model=Token, tags=["Autenticacion"])
async def login(data: LoginRequest, Authorize: AuthJWT = Depends()):
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
            raise HTTPException(status_code=503, detail=f"Servicio de usuarios invalido: {exc}")
        
    user_data = response.json()
    
    claims = {
        "roles": user_data["rol"]
    }
    
    access_token = Authorize.create_access_token(
        subject=user_data["id"],
        user_claims=claims,
        expires_time=timedelta(hours=1)
    )

        
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@app.post("/auth/logout")
def logout():
    return {"mensaje": "¡Adiós desde el Servicio Autenticacion!"}
