# servicio-reportes/main.py

from fastapi import FastAPI, Depends, HTTPException, Header
from typing import List
import httpx
from datetime import date

# Importamos lógica y schemas
from . import schemas, logic
from .config import settings

app = FastAPI(title="Servicio de Reportes y Cálculos")

# URLs de los otros microservicios (internas de Docker)
URL_USUARIOS = "http://servicio-usuarios:8000"
URL_ASISTENCIA = "http://servicio-asistencia:8000"
URL_NOMINA = "http://servicio-nomina:8000" # Para obtener las reglas del cargo

@app.get(
    "/reports/payroll-preview/{user_id}",
    response_model=schemas.PayrollCalculation,
    tags=["Reportes"]
)
async def get_payroll_calculation(
    user_id: str,
    start_date: date,
    end_date: date,
    # Necesitamos el token para reenviarlo a los otros servicios (seguridad)
    authorization: str = Header(None) 
):
    """
    Orquesta la obtención de datos y cálculo de pago para un usuario.
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Token requerido")
        
    headers = {"Authorization": authorization}

    async with httpx.AsyncClient() as client:
        # 1. Obtener datos del USUARIO (necesitamos saber su job_status_id)
        # Asumo que GET /users/{id} devuelve: { "id": 1, "name": "Pepe", "job_status_id": 5 }
        try:
            r_user = await client.get(f"{URL_USUARIOS}/users/{user_id}", headers=headers)
            r_user.raise_for_status()
            user_data = r_user.json()
            job_status_id = user_data.get("job_status_id") # O "cargo_id"
            
            if not job_status_id:
                raise HTTPException(status_code=400, detail="El usuario no tiene un Cargo/Status asignado")
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"Fallo al obtener usuario: {e}")

        # 2. Obtener reglas del CARGO/STATUS (Servicio Nómina)
        # Asumo que GET /statuses/{id} devuelve: { "base_hourly_rate": 10, ... }
        try:
            r_rules = await client.get(f"{URL_NOMINA}/statuses/{job_status_id}", headers=headers)
            r_rules.raise_for_status()
            job_rules = r_rules.json()
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"Fallo al obtener reglas de pago: {e}")

        # 3. Obtener MARCACIONES (Servicio Asistencia)
        # Este endpoint debe soportar rango de fechas
        try:
            r_marks = await client.get(
                f"{URL_ASISTENCIA}/attendance/history",
                params={"user_id": user_id, "start_date": str(start_date), "end_date": str(end_date)},
                headers=headers
            )
            r_marks.raise_for_status()
            attendance_data = r_marks.json()
        except Exception as e:
             # Si falla o no hay marcas, enviamos lista vacía para que calcule 0
            attendance_data = []

    # 4. PROCESAR LOGICA (Pandas)
    calculation = logic.calculate_monthly_payroll(attendance_data, job_rules)

    # 5. Retornar Resultado
    return {
        "user_id": str(user_id),
        "user_name": user_data.get("name", "Desconocido"),
        "job_status": job_rules.get("name", "Desconocido"),
        
        "total_regular_hours": calculation["total_regular_hours"],
        "total_overtime_hours": calculation["total_overtime_hours"],
        
        "rate_per_hour": job_rules.get("base_hourly_rate"),
        "estimated_gross_pay": calculation["gross_pay"],
        
        "details": calculation["details"]
    }