# Imagen base de Python 3.12
FROM python:3.12

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instala dependencias del sistema necesarias (ej: pymysql)
RUN apt-get update && apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

# Copia el archivo de dependencias
COPY requirements.txt .

# Instala dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el código del microservicio
COPY . .

# Expone el puerto del microservicio
EXPOSE 9003

# Comando para ejecutar el microservicio con uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9003", "--reload"]
