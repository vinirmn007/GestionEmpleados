from pydantic import BaseModel, EmailStr
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str | None = None

class RefreshTokenRequest(BaseModel):
    token: str

class RefreshToken(BaseModel):
    user_id: int
    token: str
    expire_date: datetime


class RefreshTokenInDB(RefreshToken):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class LoginRequest(BaseModel):
    email: EmailStr
    password: str