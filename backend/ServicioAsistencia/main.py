from fastapi import FastAPI, Depends, HTTPException, Request, Header
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Annotated, List
from datetime import datetime, date, timezone, timedelta
from database import Base, engine
import httpx

from verification.verify_roles import require_role

from schemas import mark_schema
from database import get_db
from crud import mark_crud as crud

app = FastAPI(title="Servicio de Asistencia")

#CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:8000", "http://127.0.0.1:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

is_employee = Depends(require_role("empleado"))
is_manager = Depends(require_role("gerente"))

USUARIOS_SERVICE_URL = "http://servicio-usuarios:9001"

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


@app.get("/attendance/reporte", response_model=list)
async def obtener_reporte_diario(
    target_date: date,
    authorization: str = Header(None),
    db: Session = Depends(get_db),
    # payload: dict = Depends(require_role("Gerente")) # Descomenta para seguridad
):
    if not authorization:
         raise HTTPException(status_code=401, detail="Token requerido para esta operación")

    # 1. Traer todos los usuarios del otro microservicio
    async with httpx.AsyncClient() as client:
        try:
            headers = {"Authorization": authorization}
            resp = await client.get(f"{USUARIOS_SERVICE_URL}/usuarios/all", headers=headers)
            resp.raise_for_status() # Lanza error si no es 200
            usuarios = resp.json()
        except Exception as e:
            raise HTTPException(status_code=503, detail="No se pudo conectar con el servicio de Usuarios")

    reporte_final = []

    # 2. Iterar usuarios y buscar sus marcas LOCALMENTE (en la BD de asistencia)
    for usuario in usuarios:
        user_id = str(usuario["id"]) # Asegúrate que los tipos coincidan (int/str)
        
        # Esta función ya la tienes en tu CRUD, úsala directo a la BD (sin HTTP)
        marcas = crud.get_marks_for_day(db, user_id, target_date)

        estado = "Adentro" if len(marcas) % 2 != 0 else "Afuera"
        
        # 3. Calcular horas AQUÍ (en Python, no en JS)
        
        # 4. Construir objeto fusionado
        fila = {
            "user_id": usuario["id"],
            "nombre": usuario["nombre"],
            "marcas": [m.timestamp for m in marcas], # Opcional: serializar marcas
            "estado": estado
        }
        reporte_final.append(fila)

    return reporte_final

@app.get("/attendance/ping")
def ping():
    return {"mensaje": "Servicio de Asistencia operativo ✅"}

Base.metadata.create_all(bind=engine)