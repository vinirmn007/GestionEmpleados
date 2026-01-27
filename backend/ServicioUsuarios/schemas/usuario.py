from typing import List
from pydantic import BaseModel, EmailStr
from enum import Enum

class RolEnum(str, Enum):
    empleado = "empleado"
    gerente = "gerente"


class UsuarioBase(BaseModel):
    nombre: str
    correo: EmailStr
    celular: str
    dni: str
    direccion: str
    rol: RolEnum  = RolEnum.empleado
    job_status_id: int | None = None

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioRead(UsuarioBase):
    id: int
    activo: bool

    class Config:
        from_attributes = True

class UserRequest(BaseModel):
    email: str
    password: str

class UserRolesResponse(BaseModel):
    roles: list[str]

class UserIdResponse(BaseModel):
    user_id: int

class PaginatedUsuarios(BaseModel):
    total: int      
    skip: int       
    limit: int      
    data: List[UsuarioRead] 
    