# servicio-nomina/main.py

import calendar
from fastapi import FastAPI, Depends, HTTPException, status, Header
from fastapi.middleware.cors import CORSMiddleware
import httpx
from sqlalchemy.orm import Session
from typing import Annotated, List
from datetime import date, timedelta

from models import models, schemas
import crud
from database import engine, get_db
from verification.verify_roles import require_role 

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Servicio de Nómina - Configuración")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

is_manager = Depends(require_role("Gerente"))

URL_REPORTES = "http://servicio-reportes-y-calculos:8000"

@app.post(
    "/statuses", 
    response_model=schemas.JobStatusResponse, 
    status_code=status.HTTP_201_CREATED,
    tags=["Gestión de Status/Cargos"]
)
async def create_job_status(
    status_data: schemas.JobStatusCreate,
    db: Annotated[Session, Depends(get_db)],
    payload: dict = is_manager
):
    existing = db.query(models.JobStatus).filter(models.JobStatus.name == status_data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Ya existe un status con ese nombre")
        
    return crud.create_status(db, status_data)

@app.get(
    "/statuses", 
    response_model=List[schemas.JobStatusResponse],
    tags=["Gestión de Status/Cargos"]
)
async def list_job_statuses(
    db: Annotated[Session, Depends(get_db)],
    payload: dict = is_manager,
    skip: int = 0, 
    limit: int = 100
):
    """
    Lista todos los status configurados y sus tarifas.
    """
    return crud.get_all_statuses(db, skip, limit)

@app.put(
    "/statuses/{status_id}", 
    response_model=schemas.JobStatusResponse,
    tags=["Gestión de Status/Cargos"]
)
async def update_job_status(
    status_id: int,
    update_data: schemas.JobStatusUpdate,
    db: Annotated[Session, Depends(get_db)],
    payload: dict = is_manager
):
    """
    Actualiza tarifas o bonos de un status existente.
    """
    updated_status = crud.update_status(db, status_id, update_data)
    if not updated_status:
        raise HTTPException(status_code=404, detail="Status no encontrado")
    return updated_status

@app.delete(
    "/statuses/{status_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Gestión de Status/Cargos"]
)
async def delete_job_status(
    status_id: int,
    db: Annotated[Session, Depends(get_db)],
    payload: dict = is_manager # <-- PROTEGIDO
):
    """
    Elimina un status.
    """
    deleted = crud.delete_status(db, status_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Status no encontrado")
    return

@app.post(
    "/payrolls/generate",
    response_model=schemas.PayrollResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Nómina (Procesos)"]
)
async def generate_payroll(
    request: schemas.PayrollGenerationRequest,
    db: Annotated[Session, Depends(get_db)],
    token_payload: dict = is_manager, # Solo Gerentes
    authorization: str = Header(None) # Necesitamos reenviar el token
):
    """
    1. Obtiene horas trabajadas (Servicio Reportes).
    2. Aplica deducciones de ley (IESS).
    3. Guarda el rol de pago en la BD.
    """
    
    # 1. Definir rango de fechas para el reporte (Mes completo)
    # Primer día del mes
    start_date = date(request.year, request.month, 1)
    # Último día del mes (ej. 28, 30, 31)
    last_day = calendar.monthrange(request.year, request.month)[1]
    end_date = date(request.year, request.month, last_day)

    # 2. Llamar al SERVICIO DE REPORTES
    # Este servicio ya hace la magia de Pandas (2 vs 4 marcas, horas x precio)
    async with httpx.AsyncClient() as client:
        try:
            # Reenviamos el token de autorización
            headers = {"Authorization": authorization}
            
            response = await client.get(
                f"{URL_REPORTES}/reports/payroll-preview/{request.user_id}",
                params={
                    "start_date": str(start_date),
                    "end_date": str(end_date)
                },
                headers=headers
            )
            response.raise_for_status()
            report_data = response.json()
            
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=f"Error en Reportes: {e.response.text}")
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"Fallo de conexión con Reportes: {e}")

    # 3. LÓGICA DE DEDUCCIONES (Reglas de Negocio Financieras)
    # El reporte nos da el "Ingreso Bruto Estimado" (estimated_gross_pay)
    gross_salary = report_data.get("estimated_gross_pay", 0.0)

    # --- PASO 3 MEJORADO: Obtener configuración de la BD ---
    
    # Buscamos la regla por su nombre clave
    iess_rule = db.query(models.DeductionRule).filter(
        models.DeductionRule.name == "IESS_PERSONAL",
        models.DeductionRule.is_active == True
    ).first()

    if not iess_rule:
        # Fallback de seguridad o Error. 
        # Opción A: Lanzar error para obligar a configurar
        raise HTTPException(status_code=500, detail="Falta configuración: IESS_PERSONAL no encontrado")
        # Opción B (menos recomendada): Usar valor por defecto
        # percentage = 9.45

    # Calculamos usando el valor de la base de datos
    # Nota: Si guardas 9.45, divide para 100. Si guardas 0.0945, úsalo directo.
    percentage_val = iess_rule.percentage / 100.0 
    
    iess_value = round(gross_salary * percentage_val, 2)
    
    # Impuesto a la Renta (Simplificado: 0 por ahora, requiere lógica compleja anual)
    tax_value = 0.0 
    
    total_deductions = iess_value + tax_value
    net_salary = gross_salary - total_deductions

    # 4. GUARDAR EN BASE DE DATOS (Persistencia)
    
    # Verificar si ya existe un rol para este mes (Evitar duplicados)
    existing_payroll = db.query(models.Payroll).filter(
        models.Payroll.user_id == request.user_id,
        models.Payroll.month == request.month,
        models.Payroll.year == request.year
    ).first()
    
    if existing_payroll:
        # Opcional: Podrías actualizarlo en lugar de lanzar error
        raise HTTPException(status_code=400, detail="El rol de pago para este mes ya fue generado.")

    new_payroll = models.Payroll(
        user_id=request.user_id,
        user_name=report_data.get("user_name"),
        month=request.month,
        year=request.year,
        
        regular_hours=report_data.get("total_regular_hours"),
        overtime_hours=report_data.get("total_overtime_hours"),
        
        gross_salary=gross_salary,
        iess_deduction=iess_value,
        tax_deduction=tax_value,
        total_deductions=total_deductions,
        net_salary=net_salary,
        
        status=models.PayrollStatus.BORRADOR, # Nace como borrador
        details_json=report_data.get("details") # Guardamos el detalle diario
    )
    
    db.add(new_payroll)
    db.commit()
    db.refresh(new_payroll)
    
    return new_payroll

@app.post(
    "/deductions",
    response_model=schemas.DeductionRuleResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Configuración Financiera"]
)
async def create_deduction_rule(
    rule_data: schemas.DeductionRuleCreate,
    db: Annotated[Session, Depends(get_db)],
    payload: dict = is_manager  # Solo gerentes
):
    """
    Crea una nueva regla de deducción (ej: IESS_PERSONAL, 9.45%).
    """
    existing = crud.get_deduction_rule_by_name(db, rule_data.name)
    if existing:
        raise HTTPException(status_code=400, detail="Ya existe una regla con ese nombre clave.")
    
    return crud.create_deduction_rule(db, rule_data)

@app.get(
    "/deductions",
    response_model=List[schemas.DeductionRuleResponse],
    tags=["Configuración Financiera"]
)
async def list_deduction_rules(
    db: Annotated[Session, Depends(get_db)],
    payload: dict = is_manager,
    skip: int = 0,
    limit: int = 100
):
    """
    Lista todas las reglas de deducción configuradas.
    """
    return crud.get_all_deduction_rules(db, skip, limit)

@app.put(
    "/deductions/{rule_id}",
    response_model=schemas.DeductionRuleResponse,
    tags=["Configuración Financiera"]
)
async def update_deduction_rule(
    rule_id: int,
    update_data: schemas.DeductionRuleUpdate,
    db: Annotated[Session, Depends(get_db)],
    payload: dict = is_manager
):
    """
    Actualiza el porcentaje o descripción de una deducción.
    """
    updated_rule = crud.update_deduction_rule(db, rule_id, update_data)
    if not updated_rule:
        raise HTTPException(status_code=404, detail="Regla de deducción no encontrada")
    return updated_rule