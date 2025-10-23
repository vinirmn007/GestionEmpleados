from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from database_config import Base
from datetime import datetime

class TokenDenylist(Base):
    __tablename__ = "token_denylist"

    #JWT ID del token revocado
    jti = Column(String(36), primary_key=True, index=True)
    create_date = Column(DateTime, default=datetime.utcnow)
