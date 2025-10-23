from pydantic import BaseModel, EmailStr
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str

#Modelos derequests
class LoginRequest(BaseModel):
    email: EmailStr
    password: str