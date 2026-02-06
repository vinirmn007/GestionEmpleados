from sqlalchemy.orm import Session
from models import models, schemas

def create_status(db: Session, status: schemas.JobStatusCreate):
    db_status = models.JobStatus(**status.dict())
    db.add(db_status)
    db.commit()
    db.refresh(db_status)
    return db_status

def get_status(db: Session, status_id: int):
    return db.query(models.JobStatus).filter(models.JobStatus.id == status_id).first()

def get_all_statuses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.JobStatus).offset(skip).limit(limit).all()

def update_status(db: Session, status_id: int, update_data: schemas.JobStatusUpdate):
    db_status = get_status(db, status_id)
    if not db_status:
        return None
    
    data = update_data.dict(exclude_unset=True)
    for key, value in data.items():
        setattr(db_status, key, value)
    
    db.add(db_status)
    db.commit()
    db.refresh(db_status)
    return db_status

def delete_status(db: Session, status_id: int):
    db_status = get_status(db, status_id)
    if db_status:
        db.delete(db_status)
        db.commit()
    return db_status

def get_deduction_rule_by_name(db: Session, name: str):
    return db.query(models.DeductionRule).filter(models.DeductionRule.name == name).first()

def get_all_deduction_rules(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.DeductionRule).offset(skip).limit(limit).all()

def create_deduction_rule(db: Session, rule: schemas.DeductionRuleCreate):
    db_rule = models.DeductionRule(
        name=rule.name,
        description=rule.description,
        percentage=rule.percentage
    )
    db.add(db_rule)
    db.commit()
    db.refresh(db_rule)
    return db_rule

def update_deduction_rule(db: Session, rule_id: int, update_data: schemas.DeductionRuleUpdate):
    db_rule = db.query(models.DeductionRule).filter(models.DeductionRule.id == rule_id).first()
    if not db_rule:
        return None
    
    # Actualizamos solo los campos que vengan en el request
    if update_data.description is not None:
        db_rule.description = update_data.description
    if update_data.percentage is not None:
        db_rule.percentage = update_data.percentage
    if update_data.is_active is not None:
        db_rule.is_active = update_data.is_active
        
    db.commit()
    db.refresh(db_rule)
    return db_rule

def get_payrolls_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
   return db.query(models.Payroll).filter(models.Payroll.user_id == user_id).order_by(models.Payroll.year.desc(), models.Payroll.month.desc()).offset(skip).limit(limit).all()