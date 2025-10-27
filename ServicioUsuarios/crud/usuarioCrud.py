from sqlalchemy.orm import Session
from models.usuario_model import Usuario
from schemas.usuario import UsuarioCreate
from utils.security import hash_password 

def get_user_by_email(db: Session, correo: str):
    return db.query(Usuario).filter(Usuario.correo == correo).first()

def get_user(db: Session, user_id: int):
    return db.query(Usuario).filter(Usuario.id == user_id).first()

def create_user(db, usuario: UsuarioCreate):
    print("DEBUG password recibido:", usuario.password, type(usuario.password))
    hashed = hash_password(usuario.password)
    db_user = Usuario(
        nombre=usuario.nombre,
        correo=usuario.correo,
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
