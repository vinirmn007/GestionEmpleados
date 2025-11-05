from pydantic import BaseModel
from datetime import datetime

class MarkResponse(BaseModel):
    id: int
    user_id: str
    timestamp: datetime

    class Config:
        orm_mode = True

class MarkStatusResponse(BaseModel):
    new_mark: MarkResponse
    current_status: str
    todays_marks: int