from sqlalchemy import Column, Integer, String, Time
from sqlalchemy.ext.declarative import declarative_base

from database import Base  # Importa Base desde database.py

class Horario(Base):
    __tablename__ = "horarios"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)  # ID del usuario (FK lógico)
    day_of_week = Column(String(10), nullable=False)  # Lunes, Martes...
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
