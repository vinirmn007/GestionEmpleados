# servicio-nomina/crud.py
from sqlalchemy.orm import Session
from models import models, schemas

def create_status(db: Session, status: schemas.JobStatusCreate):
    db_status = models.JobStatus(**status.dict())
    db.add(db_status)
    db.commit()
    db.refresh(db_status)
    return db_status

def get_status(db: Session, status_id: int):
    return db.query(models.JobStatus).filter(models.JobStatus.id == status_id).first()

def get_all_statuses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.JobStatus).offset(skip).limit(limit).all()

def update_status(db: Session, status_id: int, update_data: schemas.JobStatusUpdate):
    db_status = get_status(db, status_id)
    if not db_status:
        return None
    
    data = update_data.dict(exclude_unset=True)
    for key, value in data.items():
        setattr(db_status, key, value)
    
    db.add(db_status)
    db.commit()
    db.refresh(db_status)
    return db_status

def delete_status(db: Session, status_id: int):
    db_status = get_status(db, status_id)
    if db_status:
        db.delete(db_status)
        db.commit()
    return db_status