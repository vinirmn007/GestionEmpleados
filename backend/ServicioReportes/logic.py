import pandas as pd
from datetime import timedelta, timezone

def calculate_monthly_payroll(
    attendance_data: list, 
    job_rules: dict
) -> dict:    
    if not attendance_data:
        return {
            "total_regular_hours": 0.0,
            "total_overtime_hours": 0.0,
            "gross_pay": 0.0,
            "details": []
        }

    df = pd.DataFrame(attendance_data)
    
    # Manejo de timestamps (que ahora vienen como objetos con 'timestamp' o strings si falló algo)
    # attendance_data = [{"id": 1, "timestamp": "...", ...}, ...]
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    else:
        # fallback si viniera lista de strings (legacy)
        df = pd.DataFrame({'timestamp': attendance_data})
        df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Convertir UTC a Local (-5)
    # Suponiendo que la BD guarda en UTC. 
    # Si df['timestamp'] no tiene tz-info, asumimos que es UTC y localizamos.
    if df['timestamp'].dt.tz is None:
        df['timestamp'] = df['timestamp'].dt.tz_localize('UTC')
    
    # Convertir a zona horaria local (-5) o America/Guayaquil
    df['timestamp'] = df['timestamp'].dt.tz_convert(timezone(timedelta(hours=-5)))

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


    # Convert details dates to string for JSON serialization
    final_details = []
    for d in daily_details:
        d["date"] = str(d["date"])
        final_details.append(d)

    return {
        "total_regular_hours": round(regular_hours, 2),
        "total_overtime_hours": round(overtime_hours, 2),
        "gross_pay": round(gross_pay, 2),
        "details": final_details
    }