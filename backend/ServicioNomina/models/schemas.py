from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class JobStatusBase(BaseModel):
    name: str
    base_hourly_rate: float = Field(..., gt=0)
    overtime_rate: float = Field(..., gt=0)
    monthly_bonus: float = 0.0

class JobStatusCreate(JobStatusBase):
    pass

class JobStatusUpdate(BaseModel):
    name: Optional[str] = None
    base_hourly_rate: Optional[float] = None
    overtime_rate: Optional[float] = None
    monthly_bonus: Optional[float] = None
    is_active: Optional[bool] = None

class JobStatusResponse(JobStatusBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True