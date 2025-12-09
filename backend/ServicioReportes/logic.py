import pandas as pd
from datetime import timedelta

def calculate_monthly_payroll(
    attendance_data: list, 
    job_rules: dict
) -> dict:    
    if not attendance_data:
        return {
            "total_hours": 0.0,
            "overtime_hours": 0.0,
            "gross_pay": 0.0,
            "details": []
        }

    df = pd.DataFrame(attendance_data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    #Agrupar por fecha (día)
    df['date'] = df['timestamp'].dt.date
    daily_groups = df.groupby('date')
    
    total_hours = 0.0
    daily_details = []

    #Iterar por cada dia
    for day, group in daily_groups:
        marks = group.sort_values('timestamp')['timestamp'].tolist()
        count = len(marks)
        
        hours_today = 0.0
        status = "Error"
        
        #LOGICA DE 2 MARCAS O 4 MARCAS
        if count == 2:
            # Entrada -> Salida
            worked = marks[1] - marks[0]
            hours_today = worked.total_seconds() / 3600
            status = "Completado (Jornada Continua)"
            
        elif count == 4:
            # Entrada -> InicioLunch -> FinLunch -> Salida
            morning = marks[1] - marks[0]
            afternoon = marks[3] - marks[2]
            hours_today = (morning + afternoon).total_seconds() / 3600
            status = "Completado (Con Almuerzo)"
            
        else:
            status = "Error de Marcación"
            hours_today = 0.0

        total_hours += hours_today
        
        daily_details.append({
            "date": day,
            "status": status,
            "hours_worked": round(hours_today, 2),
            "is_overtime": hours_today > 8
        })
    
    #Calculo de horas normales y extras
    regular_hours = 0.0
    overtime_hours = 0.0
    
    for day in daily_details:
        if day["hours_worked"] > 8:
            regular_hours += 8
            overtime_hours += (day["hours_worked"] - 8)
        else:
            regular_hours += day["hours_worked"]

    #Calculo de pagos
    base_pay = regular_hours * job_rules.get('hourly_rate', 0)
    overtime_pay = overtime_hours * job_rules.get('overtime_rate', 0)
    bonus = job_rules.get('monthly_bonus', 0)
    
    gross_pay = base_pay + overtime_pay + bonus

    return {
        "total_regular_hours": round(regular_hours, 2),
        "total_overtime_hours": round(overtime_hours, 2),
        "gross_pay": round(gross_pay, 2),
        "details": daily_details
    }