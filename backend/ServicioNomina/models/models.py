# servicio-nomina/models.py
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from database import Base
from datetime import datetime

class JobStatus(Base):
    """
    Define los 'Status' o Cargos y sus reglas de pago.
    """
    __tablename__ = "job_statuses"

    id = Column(Integer, primary_key=True, index=True)
    
    # Nombre del status (ej. "Gerente", "Tiempo Completo", "Medio Tiempo")
    name = Column(String(100), unique=True, index=True, nullable=False)
    
    # Reglas financieras
    base_hourly_rate = Column(Float, nullable=False)   # Pago por hora normal
    overtime_rate = Column(Float, nullable=False)      # Pago por hora extra
    
    # Bonos fijos (opcionales)
    monthly_bonus = Column(Float, default=0.0)         # Bono de responsabilidad
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)