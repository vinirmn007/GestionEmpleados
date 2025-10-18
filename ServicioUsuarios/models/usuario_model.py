from pydantic import BaseModel, EmailStr

class Usuario(BaseModel):
    id: int
    nombres: str
    apellidos: str
    email: EmailStr
    celular: str
    rol: str
    password: str = None  


class UsuarioCreate(BaseModel):
    nombres: str
    apellidos: str
    email: EmailStr
    celular: str
    rol: str
    password: str = None

class PasswordCreate(BaseModel):
    user_id: int
    password: str

