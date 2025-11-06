from fastapi import FastAPI, Depends, HTTPException, Request, Header
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Annotated, List
from datetime import datetime, date, timezone, timedelta
import jwt

from verification.verify_roles import require_role

from .schemas import mark_schema
from .models import mark_model
from .database import engine, get_db
from .crud import mark_crud as crud

app = FastAPI(title="Servicio de Asistencia")

#CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ajustar en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependencias de rol
is_employee = Depends(require_role("Empleado"))
is_manager = Depends(require_role("Gerente"))

@app.post("/attendance/mark", response_model=mark_schema.MarkStatusResponse, tags=["Asistencia (Empleado)"])
async def create_new_mark(
    db: Annotated[Session, Depends(get_db)],
    payload: Annotated[dict, is_employee]
):
    """
    Registra una marcación (timestamp) simple.
    Determina el estado (Adentro/Afuera) contando las marcas del día.
    """
    user_id = payload.get("sub")
    timestamp = datetime.now(timezone.utc)

    # 1. Guardar la nueva marca
    new_mark = crud.create_mark(db, user_id, timestamp)

    # 2. Contar las marcas de hoy (incluida la nueva)
    marks_today = crud.get_marks_for_day(db, user_id, timestamp.date())
    mark_count = len(marks_today)

    # 3. Determinar el estado
    current_status = "Adentro" if mark_count % 2 != 0 else "Afuera"

    return mark_schema.MarkStatusResponse(
        new_mark=new_mark,
        current_status=current_status,
        todays_marks=mark_count
    )


@app.get(
    "/attendance/history",
    response_model=List[mark_schema.MarkResponse],
    tags=["Asistencia (Reportes)"]
)
async def get_attendance_history(
    user_id: str,
    target_date: date,
    db: Annotated[Session, Depends(get_db)],
    payload: Annotated[dict, is_manager]
):
    """
    Endpoint para que el Servicio de Reportes obtenga los datos crudos
    de un usuario en un día específico.
    """
    # (opcional) validar que el gerente tenga permisos sobre ese usuario
    marks = crud.get_marks_for_day(db, user_id, target_date)
    return marks


@app.get("/attendance/ping")
def ping():
    return {"mensaje": "Servicio de Asistencia operativo ✅"}