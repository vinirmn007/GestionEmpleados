from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, JSON, ForeignKey, Enum
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
import enum

# Enums para el estado del pago
class PayrollStatus(str, enum.Enum):
    BORRADOR = "Borrador"       # Calculado pero no aprobado
    PENDIENTE = "Pendiente"    # Listo para pagar
    PAGADO = "Pagado"          # Enviado al banco

class JobStatus(Base):
    """
    Define los 'Status' o Cargos y sus reglas de pago.
    """
    __tablename__ = "job_statuses"

    id = Column(Integer, primary_key=True, index=True)
    
    # Nombre del status (ej. "Gerente", "Tiempo Completo", "Medio Tiempo")
    name = Column(String(100), unique=True, index=True, nullable=False)
    
    # Reglas financieras
    base_hourly_rate = Column(Float, nullable=False)   # Pago por hora normal
    overtime_rate = Column(Float, nullable=False)      # Pago por hora extra
    
    # Bonos fijos (opcionales)
    monthly_bonus = Column(Float, default=0.0)         # Bono de responsabilidad
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Payroll(Base):
    """
    Representa un Rol de Pago guardado en la BD.
    """
    __tablename__ = "payrolls"

    id = Column(Integer, primary_key=True, index=True)
    
    user_id = Column(String(100), index=True, nullable=False)
    user_name = Column(String(200)) # Guardamos el nombre por si el usuario se borra luego
    
    # Periodo
    month = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    
    # Ingresos
    regular_hours = Column(Float, default=0.0)
    overtime_hours = Column(Float, default=0.0)
    gross_salary = Column(Float, nullable=False) # Sueldo Bruto (Ingresos totales)
    
    # Egresos / Deducciones
    iess_deduction = Column(Float, default=0.0) # Aporte personal (9.45%)
    tax_deduction = Column(Float, default=0.0)  # Impuesto a la renta
    total_deductions = Column(Float, nullable=False)
    
    # Liquido a recibir
    net_salary = Column(Float, nullable=False) # Lo que llega al banco
    
    # Auditoría y Estado
    status = Column(String(50), default=PayrollStatus.BORRADOR)
    generated_at = Column(DateTime, default=datetime.utcnow)
    paid_at = Column(DateTime, nullable=True)
    
    # Guardamos el detalle diario en JSON para auditoría futura
    # (Por si reclaman: "Faltó el día 5")
    details_json = Column(JSON, nullable=True)

class DeductionRule(Base):
    __tablename__ = "deduction_rules"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)  # Ej: "IESS_PERSONAL"
    description = Column(String(200))                    # Ej: "Aporte personal al IESS 2025"
    percentage = Column(Float)                      # Ej: 9.45 (guardado como porcentaje)
    is_active = Column(Boolean, default=True)