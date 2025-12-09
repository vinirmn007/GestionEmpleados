# servicio-nomina/main.py

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Annotated, List

from models import models, schemas
import crud
from database import engine, get_db
from verification.verify_roles import require_role 

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Servicio de Nómina - Configuración")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

is_manager = Depends(require_role("Gerente"))

@app.post(
    "/statuses", 
    response_model=schemas.JobStatusResponse, 
    status_code=status.HTTP_201_CREATED,
    tags=["Gestión de Status/Cargos"]
)
async def create_job_status(
    status_data: schemas.JobStatusCreate,
    db: Annotated[Session, Depends(get_db)],
    payload: dict = is_manager
):
    existing = db.query(models.JobStatus).filter(models.JobStatus.name == status_data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Ya existe un status con ese nombre")
        
    return crud.create_status(db, status_data)

@app.get(
    "/statuses", 
    response_model=List[schemas.JobStatusResponse],
    tags=["Gestión de Status/Cargos"]
)
async def list_job_statuses(
    db: Annotated[Session, Depends(get_db)],
    payload: dict = is_manager,
    skip: int = 0, 
    limit: int = 100
):
    """
    Lista todos los status configurados y sus tarifas.
    """
    return crud.get_all_statuses(db, skip, limit)

@app.put(
    "/statuses/{status_id}", 
    response_model=schemas.JobStatusResponse,
    tags=["Gestión de Status/Cargos"]
)
async def update_job_status(
    status_id: int,
    update_data: schemas.JobStatusUpdate,
    db: Annotated[Session, Depends(get_db)],
    payload: dict = is_manager
):
    """
    Actualiza tarifas o bonos de un status existente.
    """
    updated_status = crud.update_status(db, status_id, update_data)
    if not updated_status:
        raise HTTPException(status_code=404, detail="Status no encontrado")
    return updated_status

@app.delete(
    "/statuses/{status_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Gestión de Status/Cargos"]
)
async def delete_job_status(
    status_id: int,
    db: Annotated[Session, Depends(get_db)],
    payload: dict = is_manager # <-- PROTEGIDO
):
    """
    Elimina un status.
    """
    deleted = crud.delete_status(db, status_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Status no encontrado")
    return