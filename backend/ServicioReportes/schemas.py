from pydantic import BaseModel
from typing import List
from datetime import date

class DailyDetail(BaseModel):
    date: date
    status: str 
    hours_worked: float
    is_overtime: bool

class PayrollCalculation(BaseModel):
    user_id: str
    user_name: str
    email: str
    dni: str
    job_status: str 
    bank_account: str | None = None
    
    total_regular_hours: float
    total_overtime_hours: float
    
    rate_per_hour: float
    overtime_rate: float
    monthly_bonus: float
    estimated_gross_pay: float
    
    details: List[DailyDetail]
