from fastapi import FastAPI, Depends, HTTPException, status, Request
from datetime import timedelta
from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException

from models.models import *
from secret_keys_settings import settings

app = FastAPI(title="Servicio Autenticacion", version="1.0.0")

@app.get("/")
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

@app.post("/auth/login", response_model=Token, tags=["Autenticacion"])
def login(data: LoginRequest, Authorize: AuthJWT = Depends()):
    #LO SIGUIENTE SE OBTIENE CON EL SERVICIO DE USUARIOS
    #is_valid_user = validar que exista ese user
    #user_id = obtener el user id del usuario que hace la peticion
    #user_roles = obtener rles de usuario de la bd

    #SIMULACIONNNNNNNNNN:
    is_valid_user = False
    user_id = 1
    user_roles = ["user", "admin"]

    x = data.email
    print(x)

    if not is_valid_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos"
        )
    
    claims = {
        "roles": user_roles
    }
    
    access_token = Authorize.create_access_token(
        subject=user_id,
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