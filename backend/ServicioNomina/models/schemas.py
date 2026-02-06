from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

#statuses
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

#deduction rules
class DeductionRuleBase(BaseModel):
    name: str
    description: str | None = None
    percentage: float # 9.45

class DeductionRuleCreate(DeductionRuleBase):
    pass

class DeductionRuleUpdate(BaseModel):
    description: Optional[str] = None
    percentage: Optional[float] = None
    is_active: Optional[bool] = None

class DeductionRuleResponse(DeductionRuleBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True

#payrolls
class PayrollGenerationRequest(BaseModel):
    user_id: str
    month: int
    year: int
    override_data: Optional[dict] = None

class PayrollResponse(BaseModel):
    id: int
    user_id: str
    month: int
    year: int
    
    gross_salary: float
    total_deductions: float
    net_salary: float
    bank_account: str | None = None
    status: str
    
    generated_at: datetime

    class Config:
        orm_mode = True