from sqlalchemy import Column, Enum, Integer, String, Boolean
from schemas.usuario import RolEnum
from database import Base
from sqlalchemy import Enum as SqlEnum

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(150), unique=True, index=True, nullable=False)
    hashed_password = Column(String(256), nullable=False)
    activo = Column(Boolean, default=True)
    rol = Column(SqlEnum(RolEnum), default=RolEnum.empleado) 