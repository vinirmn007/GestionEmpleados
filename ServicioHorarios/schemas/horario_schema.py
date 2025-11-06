from pydantic import BaseModel
from datetime import time

class HorarioBase(BaseModel):
    day_of_week: str
    start_time: time
    end_time: time

class HorarioCreate(HorarioBase):
    user_id: int

class HorarioResponse(HorarioBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
