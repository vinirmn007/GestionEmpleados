# servicio-reportes/schemas.py
from pydantic import BaseModel
from typing import List
from datetime import date

class DailyDetail(BaseModel):
    date: date
    status: str # "Completado", "Falta", "Error de Marcación"
    hours_worked: float
    is_overtime: bool

class PayrollCalculation(BaseModel):
    user_id: str
    user_name: str
    job_status: str # "Gerente", "Medio Tiempo"
    
    total_regular_hours: float
    total_overtime_hours: float
    
    # Cálculos monetarios estimados
    rate_per_hour: float
    estimated_gross_pay: float
    
    details: List[DailyDetail]