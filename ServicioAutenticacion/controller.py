from sqlalchemy.orm import Session
from models import models, db_model
from datetime import datetime

#añade un token no valido o revocado a la db
def add_revoked_token(db: Session, jti: str):
    revoked_token = db_model.TokenDenylist(jti=jti, create_date=datetime.utcnow())
    db.add(revoked_token)
    db.commit()
    db.refresh(revoked_token)
    return revoked_token

#consulta si es un token no valido o revocado en db
def is_token_revoked(db: Session, jti: str):
    token = db.query(db_model.TokenDenylist).filter(db_model.TokenDenylist.jti == jti).first()
    return token is not None

#valida las credenciales del usuario
def authenticate_user(db: Session, email: str):
    #BUSCAR EN DB DE MICROSERVICIO USUARIOS
    pass