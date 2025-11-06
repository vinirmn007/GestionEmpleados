from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import Base, engine, get_db
from models.horario_model import Horario
from schemas.horario_schema import HorarioCreate, HorarioResponse, HorarioBase
from crud.horario_crud import create_horario, get_horarios_by_user, update_horario, delete_horario
import requests



# --- Inicialización ---
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Servicio de Gestión de Horarios")

USER_SERVICE_URL = "http://localhost:8001"
#USER_SERVICE_URL = "http://servicio-usuarios:9001"


def validar_usuario(user_id: int):
    url = f"{USER_SERVICE_URL}/usuarios/{user_id}"
    try:
        resp = requests.get(url)
        if resp.status_code == 404:
            raise HTTPException(status_code=404, detail="Usuario no encontrado en el servicio de usuarios")
        elif resp.status_code != 200:
            raise HTTPException(status_code=502, detail="Error al comunicarse con el servicio de usuarios")
        return resp.json()
    except requests.exceptions.RequestException:
        raise HTTPException(status_code=502, detail="No se pudo conectar al servicio de usuarios")



# --- Endpoints CRUD de Horarios ---
@app.post("/schedules/assignments", response_model=HorarioResponse, tags=["Horarios"])
def assign_schedule(horario: HorarioCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo horario y lo asigna a un usuario.
    """
    validar_usuario(horario.user_id)
    return create_horario(db, horario)


@app.get("/{user_id}/schedule", response_model=List[HorarioResponse], tags=["Horarios"])
def get_user_schedule(user_id: int, db: Session = Depends(get_db)):
    """
    Obtiene todos los horarios asignados a un usuario.
    """
    validar_usuario(user_id)
    return get_horarios_by_user(db, user_id)


@app.put("/schedules/{horario_id}", response_model=HorarioResponse, tags=["Horarios"])
def update_user_schedule(horario_id: int, updated: HorarioBase, db: Session = Depends(get_db)):
    """
    Actualiza la información de un horario existente.
    """
    horario = update_horario(db, horario_id, updated)
    if not horario:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    return horario


@app.delete("/schedules/{horario_id}", tags=["Horarios"])
def delete_user_schedule(horario_id: int, db: Session = Depends(get_db)):
    """
    Elimina un horario existente.
    """
    horario = delete_horario(db, horario_id)
    if not horario:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    return {"detail": "Horario eliminado correctamente"}
