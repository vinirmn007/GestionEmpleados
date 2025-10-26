# 1. Imagen base: Usamos una imagen oficial de Python
FROM python:3.12

# 2. Directorio de trabajo: Creamos un directorio dentro del contenedor
WORKDIR /app

# 3. Copiar dependencias: Copiamos solo el archivo de requisitos primero
#    (Esto aprovecha el caché de Docker y no reinstala todo cada vez)
COPY requirements.txt requirements.txt

# 4. Instalar dependencias: Instalamos las librerías (FastAPI, Uvicorn, etc.)
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar el código: Copiamos todo el código de tu servicio al contenedor
COPY . .

# 6. Exponer el puerto: Le decimos a Docker que el servicio usa el puerto 8000
EXPOSE 8000

# 7. Comando de inicio: Cómo ejecutar tu app. 
#    Ajusta "main:app" al nombre de tu archivo y variable de FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]