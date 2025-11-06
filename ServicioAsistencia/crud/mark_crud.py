from sqlalchemy.orm import Session
from models import mark_model
from datetime import datetime, time, date

def create_mark(db, user_id: str, timestamp: datetime) -> mark_model.Mark:
    db_mark = mark_model.Mark(
        user_id=user_id,
        timestamp=timestamp
    )
    db.add(db_mark)
    db.commit()
    db.refresh(db_mark)
    return db_mark

def get_marks_for_day(db: Session, user_id: str, target_date: date) -> list[mark_model.Mark]:
    start_of_day = datetime.combine(target_date, time.min)
    end_of_day = datetime.combine(target_date, time.max)

    return db.query(mark_model.Mark).filter(
        mark_model.Mark.user_id == user_id,
        mark_model.Mark.timestamp >= start_of_day,
        mark_model.Mark.timestamp <= end_of_day
    ).order_by(mark_model.Mark.timestamp.asc()).all()