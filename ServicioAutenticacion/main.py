from fastapi import FastAPI, Depends, HTTPException, status
from datetime import timedelta

from fastapi_jwt_auth3 import AuthJWT
#from fastapi_jwt_auth3.exceptions import AuthJWTException
from pydantic import BaseModel
from fastapi import Request
from fastapi.responses import JSONResponse

from .models import models, db_model
from .secret_keys_settings import settings

app = FastAPI(title="Servicio Autenticacion", version="1.0.0")

@app.get("/")
def read_root():
    return {"mensaje": "¡Hola, Servicio Autenticacion está funcionando!"}

@AuthJWT.load_config
def get_config():
    return settings

@app.post("auth/login", response_model=models.Token, tags=["Autenticacion"])
def login(data: models.LoginRequest, Authorize: AuthJWT = Depends()):
    #LO SIGUIENTE SE OBTIENE CON EL SERVICIO DE USUARIOS
    #is_valid_user = validar que exista ese user
    #user_id = obtener el user id del usuario que hace la peticion
    #user_roles = obtener rles de usuario de la bd

    #SIMULACIONNNNNNNNNN:
    is_valid_user = True
    user_id = 1
    user_roles = ["user", "admin"]

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
    pass

@app.post("auth/logout")
def logout():
    return {"mensaje": "¡Adiós desde el Servicio Autenticacion!"}

