from sqlalchemy.orm import Session
from models import mark_model
from datetime import datetime, time, date, timezone, timedelta

def create_mark(db: Session, user_id: str, timestamp: datetime) -> mark_model.Mark:
    db_mark = mark_model.Mark(
        user_id=user_id,
        timestamp=timestamp
    )
    db.add(db_mark)
    db.commit()
    db.refresh(db_mark)
    if db_mark.timestamp and db_mark.timestamp.tzinfo is None:
        db_mark.timestamp = db_mark.timestamp.replace(tzinfo=timezone.utc)
    return db_mark

def get_mark(db: Session, mark_id: int) -> mark_model.Mark:
    mark = db.query(mark_model.Mark).filter(mark_model.Mark.id == mark_id).first()
    if mark and mark.timestamp and mark.timestamp.tzinfo is None:
        mark.timestamp = mark.timestamp.replace(tzinfo=timezone.utc)
    return mark

def update_mark(db: Session, mark_id: int, new_timestamp: datetime) -> mark_model.Mark:
    db_mark = get_mark(db, mark_id)
    if db_mark:
        db_mark.timestamp = new_timestamp
        db.commit()
        db.refresh(db_mark)
        if db_mark.timestamp and db_mark.timestamp.tzinfo is None:
            db_mark.timestamp = db_mark.timestamp.replace(tzinfo=timezone.utc)
    return db_mark

def delete_mark(db: Session, mark_id: int) -> bool:
    db_mark = get_mark(db, mark_id)
    if db_mark:
        db.delete(db_mark)
        db.commit()
        return True
    return False

def get_marks_for_day(db: Session, user_id: str, target_date: date) -> list[mark_model.Mark]:
    # UTC+5 logic for Local Time (assuming offset -5 hours for location, so UTC day starts 05:00)
    start_of_day = datetime.combine(target_date, time.min) + timedelta(hours=5)
    end_of_day = datetime.combine(target_date, time.max) + timedelta(hours=5)

    marks = db.query(mark_model.Mark).filter(
        mark_model.Mark.user_id == user_id,
        mark_model.Mark.timestamp >= start_of_day,
        mark_model.Mark.timestamp <= end_of_day
    ).order_by(mark_model.Mark.timestamp.asc()).all()
    
    for m in marks:
        if m.timestamp and m.timestamp.tzinfo is None:
            m.timestamp = m.timestamp.replace(tzinfo=timezone.utc)
    return marks

def get_marks_in_range(db: Session, user_id: str, start_date: date, end_date: date) -> list[mark_model.Mark]:
    start_time = datetime.combine(start_date, time.min) + timedelta(hours=5)
    end_time = datetime.combine(end_date, time.max) + timedelta(hours=5)
    
    marks = db.query(mark_model.Mark).filter(
        mark_model.Mark.user_id == user_id,
        mark_model.Mark.timestamp >= start_time,
        mark_model.Mark.timestamp <= end_time
    ).order_by(mark_model.Mark.timestamp.asc()).all()

    for m in marks:
        if m.timestamp and m.timestamp.tzinfo is None:
            m.timestamp = m.timestamp.replace(tzinfo=timezone.utc)
    return marks