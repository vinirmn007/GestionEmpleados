from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from fastapi_jwt_auth3 import AuthJWT
#from fastapi_jwt_auth3.exceptions import AuthJWTException
from pydantic import BaseModel
from fastapi import Request
from fastapi.responses import JSONResponse

from .models import models, db_model
from . import controller
from .database_config import engine, get_db
from .secret_keys_settings import settings

#crea la tabla en db
db_model.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Servicio Autenticacion", version="1.0.0")

@app.get("/")
def read_root():
    return {"mensaje": "¡Hola, Servicio Autenticacion está funcionando!"}

@AuthJWT.load_config
def get_config():
    return settings

#validar si el token esta en denylist
@AuthJWT.token_in_denylist_loader
def token_in_denylist(decrypted_token: dict):
    jti = decrypted_token["jti"]
    
    db = next(get_db()) 
    
    return controller.is_token_revoked(db, jti)

@app.post("auth/login", response_model=models.Token, tags=["Autenticacion"])
def login(data: models.LoginRequest, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    
    pass

@app.post("auth/logout")
def logout():
    return {"mensaje": "¡Adiós desde el Servicio Autenticacion!"}

@app.post("auth/refresh")
def refresh_token():
    return {"mensaje": "Token de autenticación renovado"}
