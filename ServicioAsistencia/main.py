from fastapi import FastAPI, Depends, HTTPException, Request, Header
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Annotated, List
from datetime import datetime, date, timezone, timedelta

from verification.verify_roles import require_role

from schemas import mark_schema
from database import get_db
from crud import mark_crud as crud

app = FastAPI(title="Servicio de Asistencia")

#CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

is_employee = Depends(require_role("Empleado"))
is_manager = Depends(require_role("Gerente"))

@app.post("/attendance/mark", response_model=mark_schema.MarkStatusResponse, tags=["Asistencia (Empleado)"])
async def create_new_mark(db: Annotated[Session, Depends(get_db)],payload: Annotated[dict, is_employee]):
    user_id = payload.get("sub")
    timestamp = datetime.now(timezone.utc)

    new_mark = crud.create_mark(db, user_id, timestamp)

    marks_today = crud.get_marks_for_day(db, user_id, timestamp.date())
    mark_count = len(marks_today)

    current_status = "Adentro" if mark_count % 2 != 0 else "Afuera"

    return mark_schema.MarkStatusResponse(
        new_mark=new_mark,
        current_status=current_status,
        todays_marks=mark_count
    )

@app.post("/attendance/mark/test", response_model=mark_schema.MarkStatusResponse, tags=["Asistencia (Empleado)"])
async def create_new_mark_test(db: Annotated[Session, Depends(get_db)], user_id: str):
    timestamp = datetime.now(timezone.utc)

    new_mark = crud.create_mark(db, user_id, timestamp)

    marks_today = crud.get_marks_for_day(db, user_id, timestamp.date())
    mark_count = len(marks_today)

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
    #validar que el gerente tenga permisos sobre ese usuario
    marks = crud.get_marks_for_day(db, user_id, target_date)
    return marks


@app.get("/attendance/ping")
def ping():
    return {"mensaje": "Servicio de Asistencia operativo ✅"}