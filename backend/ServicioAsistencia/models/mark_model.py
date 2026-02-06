from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime

class Mark(Base):
    __tablename__ = "marks"

    id = Column(Integer, primary_key=True)
    user_id = Column(String(100), index=True, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)