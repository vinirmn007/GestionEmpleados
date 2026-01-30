from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import io
from datetime import date

def generate_payroll_pdf(data: dict) -> bytes:
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Titulo
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, height - 50, "Rol de Pago Individual")
    
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 70, f"Fecha de Generación: {date.today()}")

    # Datos del Empleado
    y = height - 120
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Información del Empleado")
    
    y -= 25
    c.setFont("Helvetica", 11)
    
    c.drawString(50, y, f"Nombre: {data.get('user_name')}")
    c.drawString(300, y, f"Cédula: {data.get('dni')}")
    y -= 20
    c.drawString(50, y, f"Correo: {data.get('email')}")
    c.drawString(300, y, f"Cargo: {data.get('job_status')}")
    y -= 20
    c.drawString(50, y, f"Cuenta Bancaria: {data.get('bank_account') or 'No registrada'}")
    
    # Detalle de Ingresos
    y -= 40
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Ingresos")
    y -= 25
    c.setFont("Helvetica", 11)
    
    c.drawString(50, y, f"Horas Normales ({data.get('total_regular_hours')}):")
    c.drawRightString(500, y, f"$ {data.get('base_pay', 0.0):.2f}") # Need to calculate base_pay in main or pass it
    y -= 20
    c.drawString(50, y, f"Horas Extras ({data.get('total_overtime_hours')}):")
    c.drawRightString(500, y, f"$ {data.get('overtime_pay', 0.0):.2f}")
    y -= 20
    c.drawString(50, y, "Bono Mensual:")
    c.drawRightString(500, y, f"$ {data.get('bonus', 0.0):.2f}")
    
    y -= 10
    c.line(50, y, 500, y)
    y -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Total Ingresos:")
    c.drawRightString(500, y, f"$ {data.get('estimated_gross_pay', 0.0):.2f}")

    # Detalle de Egresos (Estimado IESS)
    # Nota: Aqui solo tenemos el estimado porque reporte calcula, pero Nomina aplica las reglas reales.
    # Vamos a usar lo que tenemos.
    gross = data.get('estimated_gross_pay', 0.0)
    iess_est = gross * 0.0945 # Valor quemado por defecto si no viene
    
    y -= 50
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "Deducciones Estimadas")
    y -= 25
    c.setFont("Helvetica", 11)
    
    c.drawString(50, y, "Aporte IESS (9.45%):")
    c.drawRightString(500, y, f"$ {iess_est:.2f}")
    
    y -= 10
    c.line(50, y, 500, y)
    y -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Total Deducciones:")
    c.drawRightString(500, y, f"$ {iess_est:.2f}")
    
    # Liquido
    y -= 40
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(colors.blue)
    c.drawString(50, y, "Total a Recibir:")
    c.drawRightString(500, y, f"$ {gross - iess_est:.2f}")
    
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer.getvalue()
