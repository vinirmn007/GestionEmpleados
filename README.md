Gestion de Empleados
Carrera de Computación | UNL

GRUPO 8
- Josue Torres
- Alexis Roman

Requerimientos del proyecto.  

Python 3.12.6  
FastAPI 0.0.13  

Arquitectura seleccionada.  
Estándares de codificación adoptados.  
Flujo de trabajo con GitFlow.  
Instrucciones de ejecución.  

1. Instalar python 3.12.6  

2. Crear un entorno virtual para la ejecucion de FastAPI, de la siguiente manera:  
Para Windows: 
- Abre PowerShell o CMD en la carpeta de tu proyecto.  
- Crea el entorno virtual (ejemplo: .venv como nombre de carpeta):  
python -m venv .venv  
- Activa el entorno virtual:  
.\.venv\Scripts\activate  

Para Linux:  
- Entra a tu proyecto:  
cd ruta/a/mi/proyecto  
- Crea el entorno virtual:  
python3.12 -m venv .venv  
- Activa el entorno virtual:  
source .venv/bin/activate  

3. Instalar FastAPI:  
pip install "fastapi[standard]"

4. Ejecutar el proyecto:  
fastapi dev main.py