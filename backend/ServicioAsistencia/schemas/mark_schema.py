from pydantic import BaseModel, ConfigDict
from datetime import datetime

class MarkResponse(BaseModel):
    id: int
    user_id: str
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)

class MarkStatusResponse(BaseModel):
    new_mark: MarkResponse
    current_status: str
    todays_marks: int