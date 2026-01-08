from sqlalchemy.orm import Session
from models.usuario_model import Usuario
from schemas.usuario import UsuarioCreate
from utils.security import hash_password, verify_password

def get_user_by_email(db: Session, correo: str):
    return db.query(Usuario).filter(Usuario.correo == correo).first()

def get_user_by_dni(db: Session, dni: str):
    return db.query(Usuario).filter(Usuario.dni == dni).first()

def get_user_by_celular(db: Session, celular: str):
    return db.query(Usuario).filter(Usuario.celular == celular).first()

def verify_user_password(db: Session, correo: str, password: str):
    user = get_user_by_email(db, correo)
    if not user:
        return False
    return verify_password(password, user.hashed_password)

def get_user(db: Session, user_id: int):
    return db.query(Usuario).filter(Usuario.id == user_id).first()

def create_user(db, usuario: UsuarioCreate):
    print("DEBUG password recibido:", usuario.password, type(usuario.password))
    hashed = hash_password(usuario.password)
    db_user = Usuario(
        nombre=usuario.nombre,
        correo=usuario.correo,
        celular=usuario.celular,
        dni=usuario.dni,
        direccion=usuario.direccion,
        hashed_password=hashed,
        activo=True,
        rol=usuario.rol,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, **kwargs):
    u = get_user(db, user_id)
    if not u:
        return None
    for key, value in kwargs.items():
        setattr(u, key, value)
    db.commit()
    db.refresh(u)
    return u

def delete_user(db: Session, user_id: int):
    u = get_user(db, user_id)
    if not u:
        return None
    db.delete(u)
    db.commit()
    return u

def get_usuarios_paginated(db: Session, skip: int = 0, limit: int = 10):
    query = db.query(Usuario)
    total = query.count()
    usuarios = query.offset(skip).limit(limit).all()
    return total, usuarios