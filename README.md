# Sistema de Gestión de Empleados

**Carrera de Computación | UNL**
**Computación**

## Grupo 8
- Josue Torres
- Alexis Roman

---

## Descripción del Proyecto
Este es un **Sistema Integral de Gestión de Empleados** diseñado bajo una arquitectura de **microservicios**. El sistema permite administrar usuarios, roles de pago, control de asistencia (con validación biométrica en móvil) y gestión de horarios.

La solución se compone de tres partes principales:
1.  **Backend de Microservicios**: Expuestos a través de un API Gateway (Kong).
2.  **Aplicación Móvil**: Desarrollada en Flutter para empleados (marcación de asistencia, visualización de roles y horarios).
3.  **Frontend Web**: Panel administrativo (Svelte).

---

## Arquitectura y Tecnologías

### Backend (Microservicios)
Desarrollado en **Python (FastAPI)** y contenerizado con **Docker**.
- **Servicio Usuarios**: Gestión de perfiles y autenticación (JWT).
- **Servicio Asistencia**: Registro de marcaciones de entrada/salida.
- **Servicio Nómina**: Generación y consulta de roles de pago.
- **Servicio Horarios**: Gestión de turnos laborales.
- **API Gateway**: **Kong Gateway** para enrutamiento unificado.
- **Base de Datos**: **MariaDB**.

### Móvil
Desarrollada en **Flutter**.
- Autenticación Biométrica.
- Geolocalización para marcaciones.
- Consumo de API REST segura.

---

## Instrucciones de Despliegue

### 1. Backend (Docker)
La forma más sencilla de ejecutar todo el backend es utilizando Docker Compose.

**Requisitos**: Docker Desktop instalado.

```bash
# Navegar a la carpeta del backend (si aplica) o raíz
cd backend

# Levantar todos los servicios
docker-compose up --build -d
```
Esto iniciará:
- MariaDB (Base de datos)
- Kong Gateway (Puerto 8000)
- Todos los microservicios (Puertos 9000-9005)

### 2. Aplicación Móvil
**Requisitos**: Flutter SDK instalado.

```bash
cd mobile

# Instalar dependencias
flutter pub get

# Ejecutar en modo debug (con dispositivo conectado)
flutter run

# Generar APK para producción
flutter build apk --release
```
_Nota: El APK generado se encuentra como `app-release.apk` en la ruta base del proyecto._

### 3. Frontend Web (Svelte)
**Requisitos**: Node.js instalado.

```bash
cd frontend

# Instalar dependencias
npm install

# Ejecutar en modo desarrollo
npm run dev
```
_El panel administrativo estará disponible en `http://localhost:5173` (o el puerto que indique la consola)._

---

## Video Demostrativo
Puedes ver una demostración completa del funcionamiento del sistema en el siguiente enlace:

[**Ver Video Demostrativo en Google Drive**](https://drive.google.com/file/d/1ELcos1lknoxxnzZ0tGsjsFpZXiHZBo3E/view?usp=sharing)
