# Gestión de Empleados
**Carrera de Computación | UNL**

## Grupo 8
- Josue Torres
- Alexis Roman

---

## Requerimientos del Proyecto
- **Python**: 3.12.6  
- **FastAPI**: 0.0.13  

---

## Arquitectura Seleccionada
Se implementará la **arquitectura de microservicios**, utilizando principalmente el framework **FastAPI**, aunque no se descarta el uso de otras tecnologías según las necesidades del proyecto.

---

## Estándares de Codificación Adoptados
Se seguirán estándares basados en **legibilidad, consistencia, escalabilidad y descriptividad**:

- Uso de **CamelCase** para nombres de variables y funciones.
- Uso correcto de **sangrías**.
- Inclusión de **comentarios descriptivos**.
- **Modularización** de los componentes.

---

## Flujo de Trabajo con GitFlow
Se implementará **GitFlow**, utilizando las siguientes ramas para gestionar los cambios:

- `main`
- `develop`
- `feature/...`

---

## Instrucciones de Ejecución

### 1. Instalar Python 3.12.6
Descargar e instalar la versión 3.12.6 desde la página oficial de Python.

### 2. Crear un Entorno Virtual

#### En Windows:
- Abre PowerShell o CMD en la carpeta de tu proyecto.  
- Crea el entorno virtual (ejemplo: .venv como nombre de carpeta):  
```python -m venv .venv```  
- Activa el entorno virtual:  
```.\.venv\Scripts\activate```  

### En Linux:  
- Entra a tu proyecto:  
```cd ruta/al/proyecto```  
- Crea el entorno virtual:  
```python3.12 -m venv .venv```  
- Activa el entorno virtual:  
```source .venv/bin/activate```  

### 3. Instalar FastAPI:  
```pip install "fastapi[standard]"```

### 4. Ejecutar el proyecto:  
```fastapi dev main.py```

## Instalar MariaDB  
```sudo apt update```  
```sudo apt install mariadb-server mariadb-client```  
```sudo mariadb-secure-installation```  
Verificar la instalacion:  
```mariadb -u root -p```  

## Crear Bases de Datos necesarias
Creamos un usuario llamado: ```fastapi_user``` con contraseña: ```12345```   
```CREATE USER 'fastapi_user'@'localhost' IDENTIFIED BY '12345';```  
Creamos la Base de datos para cada microservicio, por ejemplo:
```CREATE DATABASE servicio_usuarios;```  
Concedemos permisos:  
```GRANT ALL PRIVILEGES ON servicio_usuarios.* TO 'fastapi_user'@'localhost';```  
```FLUSH PRIVILEGES;```  
