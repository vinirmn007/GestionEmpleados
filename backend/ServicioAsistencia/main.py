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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

is_employee = Depends(require_role("empleado"))
is_manager = Depends(require_role("gerente"))

USUARIOS_SERVICE_URL = "http://servicio-usuarios:9001"

async def get_current_user_multi_role(payload_empl: dict = Depends(require_role("empleado", auto_error=False)), payload_mgr: dict = Depends(require_role("gerente", auto_error=False))):
    if payload_empl:
        return payload_empl
    if payload_mgr:
        return payload_mgr
    raise HTTPException(status_code=401, detail="Se requiere rol de Empleado o Gerente")

@app.post("/attendance/mark", response_model=mark_schema.MarkStatusResponse, tags=["Asistencia (Empleado)"])
async def create_new_mark(db: Annotated[Session, Depends(get_db)], payload: dict = Depends(get_current_user_multi_role)):
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

@app.post("/attendance/mark/manual", response_model=mark_schema.MarkResponse, tags=["Asistencia (Gerente)"])
async def create_manual_mark(
    mark_data: mark_schema.MarkCreateManual,
    db: Annotated[Session, Depends(get_db)],
    payload: dict = Depends(require_role("gerente"))
):
    new_mark = crud.create_mark(db, mark_data.user_id, mark_data.timestamp)
    return new_mark

@app.put("/attendance/mark/{mark_id}", response_model=mark_schema.MarkResponse, tags=["Asistencia (Gerente)"])
async def update_mark(
    mark_id: int,
    mark_data: mark_schema.MarkUpdate,
    db: Annotated[Session, Depends(get_db)],
    payload: dict = Depends(require_role("gerente"))
):
    updated_mark = crud.update_mark(db, mark_id, mark_data.timestamp)
    if not updated_mark:
        raise HTTPException(status_code=404, detail="Marca no encontrada")
    return updated_mark

@app.delete("/attendance/mark/{mark_id}", tags=["Asistencia (Gerente)"])
async def delete_mark(
    mark_id: int,
    db: Annotated[Session, Depends(get_db)],
    payload: dict = Depends(require_role("gerente"))
):
    success = crud.delete_mark(db, mark_id)
    if not success:
        raise HTTPException(status_code=404, detail="Marca no encontrada")
    return {"message": "Marca eliminada correctamente"}

@app.get(
    "/attendance/history",
    response_model=List[mark_schema.MarkResponse],
    tags=["Asistencia (Reportes)"]
)
async def get_attendance_history(
    user_id: str,
    db: Annotated[Session, Depends(get_db)],
    payload: Annotated[dict, is_manager],
    target_date: date = None,
    start_date: date = None,
    end_date: date = None
):
    #validar que el gerente tenga permisos sobre ese usuario
    if start_date and end_date:
        return crud.get_marks_in_range(db, user_id, start_date, end_date)
    
    if target_date:
        return crud.get_marks_for_day(db, user_id, target_date)
        
    raise HTTPException(status_code=400, detail="Debe proporcionar target_date O (start_date y end_date)")


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
            "marcas": [{"id": m.id, "timestamp": m.timestamp} for m in marcas], 
            "estado": estado
        }
        reporte_final.append(fila)

    return reporte_final

@app.get("/attendance/ping")
def ping():
    return {"mensaje": "Servicio de Asistencia operativo ✅"}

Base.metadata.create_all(bind=engine)