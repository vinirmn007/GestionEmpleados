from pydantic import BaseModel, EmailStr
from enum import Enum

class RolEnum(str, Enum):
    empleado = "empleado"
    gerente = "gerente"


class UsuarioBase(BaseModel):
    nombre: str
    correo: EmailStr
    rol: RolEnum  = RolEnum.empleado

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioRead(UsuarioBase):
    id: int
    activo: bool

    class Config:
        from_attributes = True

class UserRequest(BaseModel):
    email: str

class UserRolesResponse(BaseModel):
    roles: list[str]

class UserIdResponse(BaseModel):
    user_id: int
