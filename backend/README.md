# Sistema de Gestión de Empleados - Backend

Este repositorio contiene el backend para el Sistema de Gestión de Empleados. El sistema está construido bajo una arquitectura de microservicios, diseñado para ser escalable, mantenible y robusto, gestionando todo, desde la autenticación de usuarios hasta el procesamiento de la nómina.

## Arquitectura Técnica

El backend sigue un patrón de **arquitectura de microservicios**. Cada dominio de negocio (usuarios, asistencia, nómina) está encapsulado en su propio servicio independiente.

La comunicación externa es manejada por un **API Gateway (Kong)**, que actúa como el único punto de entrada para todas las peticiones del cliente (la aplicación web y la aplicación móvil), proporcionando enrutamiento, seguridad y balanceo de carga.

### Tecnologías Principales

* **Lenguaje:** Python 3.11+
* **Framework de API:** FastAPI
* **Base de Datos:** MariaDB (con un esquema separado por servicio)
* **API Gateway:** Kong
* **Contenerización:** Docker y Docker Compose
* **Autenticación:** JWT (Access Tokens + Refresh Tokens) con "denylist" para el logout.

### Microservicios

| Servicio | Propósito | Base de Datos |
| :--- | :--- | :--- |
| **`api-gateway-kong`** | Punto de entrada único. Enruta peticiones a los servicios internos. | N/A |
| **`servicio-autenticacion`** | Gestiona el login, logout y refresco de tokens JWT. Maneja la "denylist" de tokens. | `db_auth` |
| **`servicio-usuarios`** | Gestiona la información de empleados/gerentes y sus roles (RBAC). | `db_usuarios` |
| **`servicio-asistencia`** | Registra las marcaciones (timestamps) crudas de los empleados. | `db_asistencia` |
| **`servicio-gestion-horarios`** | Define los turnos, horarios esperados y reglas de negocio. | `db_horarios` |
| **`servicio-reportes-y-calculos`** | Interpreta las marcas crudas y aplica la lógica (2 vs 4 marcas) para calcular horas. | N/A (solo lee) |
| **`servicio-nomina`** | Calcula el rol de pago basándose en los reportes y se integra con el gestor externo. | `db_nomina` |
| **`servicio-notificaciones`** | Envía alertas (push, email) a los usuarios. | `db_notificaciones` |

---

## Guía de Instalación Local

El proyecto está 100% contenerizado, por lo que no es necesario instalar Python o MariaDB localmente.

### Prerrequisitos

* [Docker](https://www.docker.com/get-started)
* [Docker Compose](https://docs.docker.com/compose/install/) (usualmente incluido con Docker Desktop)

### Pasos de Instalación

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/vinirmn007/GestionEmpleados.git](https://github.com/vinirmn007/GestionEmpleados.git)
    cd GestionEmpleados
    ```

2.  **Configurar Variables de Entorno:**
    Cada microservicio (ej. `servicio-autenticacion`, `servicio-usuarios`, etc.) tiene su propio archivo `.env`. Debes asegurarte de que existan y contengan las claves correctas.

    **Ejemplo (`servicio-autenticacion/.env`):**
    ```ini
    # Clave secreta para firmar los JWT. DEBE SER LA MISMA EN TODOS LOS SERVICIOS.
    AUTHJWT_SECRET_KEY="alexisjosue12345"

    # Credenciales de la BD (leídas de docker-compose)
    DB_HOST="db-sge"
    DB_USER="root"
    DB_PASSWORD="al.22825" 
    ```
    *Copia este archivo `.env` en cada carpeta de microservicio.*

3.  **Configurar la Contraseña de la Base de Datos:**
    Abre el archivo `docker-compose.yml` y asegúrate de que la contraseña en `MARIADB_ROOT_PASSWORD` coincida con la `DB_PASSWORD` que pusiste en tus archivos `.env`.

    **`docker-compose.yml` (fragmento):**
    ```yaml
    services:
      db-sge:
        environment:
          MARIADB_ROOT_PASSWORD: "al.22825" # <-- Esta contraseña
    ```

4.  **Construir e Iniciar los Contenedores:**
    Este es el único comando que necesitas. Construirá las imágenes de cada servicio e iniciará todo el entorno.

    ```bash
    docker-compose up --build
    ```

5.  **¡Listo!**
    El sistema completo estará corriendo.
    * **Tu API Gateway** está escuchando en `http://localhost:80`.
    * **La API de Admin de Kong** está en `http://localhost:8001`.
    * **Tu App Web (Flask)** está en `http://localhost:5000`.

---

## Endpoints de la API (Rutas del Gateway)

Todas las peticiones deben dirigirse al API Gateway (`http://localhost`). Kong se encarga de redirigirlas al servicio interno correspondiente.

### Servicio de Autenticación (`/auth`)

* **`POST /auth/login`**:
    Inicia sesión con `email` y `password`. Devuelve un `access_token` (corta duración) y un `refresh_token` (larga duración).
**LO SIGUIENTE SE IMPLEMENTARA A FUTURO**
* **`POST /auth/refresh`**:
    Requiere un `refresh_token` válido. Devuelve un nuevo `access_token` y el mismo `refresh_token`.
* **`POST /auth/logout`**:
    Requiere un `refresh_token` válido. Lo añade a la "denylist" (lista de denegación) para invalidar la sesión.

### Servicio de Usuarios (`/users`)

* **`POST /users`**:
    Creación de un nuevo usuario (empleado o gerente). Requiere rol de Gerente.
* **`GET /users`**:
    Obtiene una lista paginada de todos los usuarios. Requiere rol de Gerente.
* **`GET /users/me`**:
    Obtiene el perfil completo del usuario actualmente autenticado (basado en el token).
* **`GET /users/{user_id}`**:
    Obtiene los detalles de un usuario específico. Requiere rol de Gerente.
* **`POST /roles`**:
    Crea un nuevo rol en el sistema (ej. "Contador"). Requiere rol de Admin.
* **`GET /roles`**:
    Lista todos los roles disponibles.

### Servicio de Gestión de Horarios (`/schedules`)

* **`POST /schedules/templates`**:
    Crea una nueva plantilla de horario (ej. "Turno Mañana 8-5"). Requiere rol de Gerente.
* **`GET /schedules/templates`**:
    Lista todas las plantillas de horarios disponibles.
* **`POST /schedules/assignments`**:
    Asigna una plantilla de horario (`template_id`) a un empleado (`user_id`) a partir de una fecha. Requiere rol de Gerente.
* **`GET /users/{user_id}/schedule`**:
    Obtiene el horario asignado para un empleado en una fecha específica.

### Servicio de Asistencia (`/attendance`)

* **`POST /attendance/mark`**:
    Registra una marcación (timestamp) cruda para el empleado autenticado. El servicio solo guarda la hora.
* **`GET /attendance/history?user_id=...&target_date=...`**:
    (Ruta interna/para Gerentes) Obtiene la lista de marcas crudas de un usuario en un día específico. Usada por el servicio de reportes.

### Servicio de Reportes y Cálculos (`/reports`)

* **`GET /reports/daily-summary/{user_id}?target_date=...`**:
    Interpreta las marcas crudas de un día y aplica la lógica de 2 vs 4 marcas. Devuelve el total de horas trabajadas y el estado (ej. "Error de marcación").
* **`GET /reports/team-attendance`**:
    Muestra el estado actual de todos los empleados (quién está "Adentro" y quién "Afuera"). Requiere rol de Gerente.
* **`GET /reports/team-punctuality?month=...&year=...`**:
    Genera un reporte de atrasos para el equipo. Requiere rol de Gerente.

### Servicio de Nómina (`/payrolls`)

* **`POST /payrolls/generate?month=...&year=...`**:
    (Para Gerentes) Inicia el pre-cálculo de la nómina de un período. Llama al servicio de reportes para obtener las horas.
* **`POST /payrolls/submit`**:
    (Para Gerentes) Aprueba la nómina pre-calculada y la envía al sistema de pagos externo.
* **`GET /payrolls/{payroll_id}`**:
    Obtiene el detalle de un rol de pago específico.
* **`GET /users/me/payrolls`**:
    (Para Empleados) Obtiene el historial de roles de pago del propio usuario.

### Servicio de Notificaciones (`/notifications`)

* **`POST /notifications/register-device`**:
    Registra el token de un dispositivo móvil (para notificaciones push).
* **`GET /notifications`**:
    Obtiene las últimas notificaciones (leídas y no leídas) para el usuario autenticado.
* **`POST /notifications/mark-read`**:
    Marca una o varias notificaciones como leídas.
