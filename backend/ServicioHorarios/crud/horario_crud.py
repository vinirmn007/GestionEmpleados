from sqlalchemy.orm import Session
from models.horario_model import Horario
from schemas.horario_schema import HorarioCreate, HorarioBase

def create_horario(db: Session, horario: HorarioCreate):
    db_horario = Horario(
        user_id=horario.user_id,
        day_of_week=horario.day_of_week,
        start_time=horario.start_time,
        end_time=horario.end_time
    )
    db.add(db_horario)
    db.commit()
    db.refresh(db_horario)
    return db_horario

def get_horarios_by_user(db: Session, user_id: int):
    return db.query(Horario).filter(Horario.user_id == user_id).all()

def get_horario_by_id(db: Session, horario_id: int):
    return db.query(Horario).filter(Horario.id == horario_id).first()

def update_horario(db: Session, horario_id: int, updated: HorarioBase):
    horario = db.query(Horario).filter(Horario.id == horario_id).first()
    if horario:
        horario.day_of_week = updated.day_of_week
        horario.start_time = updated.start_time
        horario.end_time = updated.end_time
        db.commit()
        db.refresh(horario)
    return horario

def delete_horario(db: Session, horario_id: int):
    horario = db.query(Horario).filter(Horario.id == horario_id).first()
    if horario:
        db.delete(horario)
        db.commit()
    return horario
