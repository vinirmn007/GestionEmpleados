from fastapi import FastAPI, Depends, HTTPException, Header, Response
from typing import List
import httpx
from datetime import date
import os

import schemas, logic, pdf_utils

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Servicio de Reportes y Cálculos")

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#URLs de los otros microservicios
URL_USUARIOS = os.getenv("URL_USUARIOS", "http://servicio-usuarios:9001")
URL_ASISTENCIA = os.getenv("URL_ASISTENCIA", "http://servicio-asistencia:9002")
URL_NOMINA = os.getenv("URL_NOMINA", "http://servicio-nomina:9004")

@app.get(
    "/reports/payroll-preview/{user_id}",
    response_model=schemas.PayrollCalculation,
    tags=["Reportes"]
)
async def get_payroll_calculation(
    user_id: str,
    start_date: date,
    end_date: date,
    authorization: str = Header(None) 
):
    """
    Orquesta la obtención de datos y cálculo de pago para un usuario.
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Token requerido")
        
    headers = {"Authorization": authorization}

    async with httpx.AsyncClient() as client:
        #Obtener datos del USUARIO (necesitamos saber su job_status_id)
        try:
            r_user = await client.get(f"{URL_USUARIOS}/usuarios/get/{user_id}", headers=headers)
            r_user.raise_for_status()
            user_data = r_user.json()
            job_status_id = user_data.get("job_status_id")
            bank_account = user_data.get("numero_cuenta")
            
            if not job_status_id:
                raise HTTPException(status_code=400, detail="El usuario no tiene un Cargo/Status asignado")
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"Fallo al obtener usuario: {e}")

        #Obtener reglas del status (Servicio nomina)
        try:
            r_rules = await client.get(f"{URL_NOMINA}/statuses/{job_status_id}", headers=headers)
            r_rules.raise_for_status()
            job_rules = r_rules.json()
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"Fallo al obtener reglas de pago: {e}")

        #Obtener MARCACIONES (Servicio Asistencia)
        try:
            r_marks = await client.get(
                f"{URL_ASISTENCIA}/attendance/history",
                params={"user_id": user_id, "start_date": str(start_date), "end_date": str(end_date)},
                headers=headers
            )
            r_marks.raise_for_status()
            attendance_data = r_marks.json()
        except Exception as e:
            attendance_data = []

    #Procesar datos y calcular pago
    calculation = logic.calculate_monthly_payroll(attendance_data, job_rules)

    #retornar json
    return {
        "user_id": str(user_id),
        "user_name": user_data.get("nombre", "Desconocido"),
        "email": user_data.get("correo", ""),
        "dni": user_data.get("dni", ""),
        "job_status": job_rules.get("name", "Desconocido"),
        "job_status": job_rules.get("name", "Desconocido"),
        "bank_account": bank_account,
        
        "total_regular_hours": calculation["total_regular_hours"],
        "total_overtime_hours": calculation["total_overtime_hours"],
        
        "rate_per_hour": job_rules.get("base_hourly_rate", 0),
        "overtime_rate": job_rules.get("overtime_rate", 0),
        "monthly_bonus": job_rules.get("monthly_bonus", 0),
        "estimated_gross_pay": calculation["gross_pay"],
        
        "details": calculation["details"]
    }

@app.post("/reports/pdf", tags=["Reportes"])
async def generate_pdf_endpoint(data: schemas.PayrollCalculation):
    try:
        pdf_bytes = pdf_utils.generate_payroll_pdf(data.dict())
        return Response(content=pdf_bytes, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=rol_pago.pdf"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando PDF: {e}")