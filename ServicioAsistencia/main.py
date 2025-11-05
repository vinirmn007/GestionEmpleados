from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Annotated, List
from datetime import datetime, date

from fastapi_jwt_auth3 import AuthJWT
from fastapi_jwt_auth3.exceptions import AuthJWTException

from .models import schemas
from . import models, crud
from .database import engine, get_db
from .config import settings

# --- Creación de la App y Tablas ---
models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="Servicio de Asistencia")

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Cambia esto en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Configuración de JWT (Debe ser idéntica a la de auth) ---
@AuthJWT.load_config
def get_config():
    return settings

@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})

# --- Dependencia de Roles ---
def require_role(role: str):
    def check_role(Auth: AuthJWT = Depends()):
        Auth.jwt_required()
        claims = Auth.get_jwt()
        user_roles = claims.get("roles", [])
        if role not in user_roles:
            raise HTTPException(status_code=403, detail=f"Se requiere rol '{role}'")
        return Auth
    return check_role

is_employee = Depends(require_role("Empleado"))
is_manager = Depends(require_role("Gerente"))

# --- Endpoints ---

@app.post(
    "/attendance/mark", 
    response_model=schemas.MarkStatusResponse,
    tags=["Asistencia (Empleado)"]
)
async def create_new_mark(
    db: Annotated[Session, Depends(get_db)],
    Auth: Annotated[AuthJWT, is_employee]
):
    """
    Registra una marcación (timestamp) simple.
    Determina el estado (Adentro/Afuera) contando las marcas del día.
    """
    user_id = Auth.get_jwt_subject()
    timestamp = datetime.utcnow()
    
    # 1. Guardar la nueva marca
    new_mark = crud.create_mark(db, user_id, timestamp)
    
    # 2. Contar las marcas de hoy (incluida la nueva)
    marks_today = crud.get_marks_for_day(db, user_id, timestamp.date())
    mark_count = len(marks_today)
    
    # 3. Determinar el estado
    # Si el número de marcas es impar (1, 3), está "Adentro".
    # Si es par (2, 4), está "Afuera".
    current_status = "Adentro" if mark_count % 2 != 0 else "Afuera"
            
    return schemas.MarkStatusResponse(
        new_mark=new_mark,
        current_status=current_status,
        todays_marks=mark_count
    )

@app.get(
    "/attendance/history", 
    response_model=List[schemas.MarkResponse],
    tags=["Asistencia (Reportes)"]
)
async def get_attendance_history(
    user_id: str, # El ID del usuario a consultar
    target_date: date, # La fecha (ej. 2025-11-05)
    db: Annotated[Session, Depends(get_db)],
    Auth: Annotated[AuthJWT, is_manager] # Protegido para Gerentes/Servicios
):
    """
    Endpoint para que el Servicio de Reportes obtenga los datos crudos
    de un usuario en un día específico.
    """
    # Aquí faltaría validar que el Gerente pueda ver a ese user_id
    marks = crud.get_marks_for_day(db, user_id, target_date)
    return marks