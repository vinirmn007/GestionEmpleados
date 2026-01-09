# Sistema de Gestión de Empleados - Frontend Web

Este repositorio contiene la capa de presentación (Frontend) del Sistema de Gestión de Empleados[cite: 6]. [cite_start]El proyecto ha sido desarrollado como el segundo hito integrador, conectando una interfaz web responsiva con el backend mediante servicios API REST.

## Información del Proyecto

**Universidad:** Universidad Nacional de Loja.
**Carrera:** Computación.
**Asignatura:** Desarrollo Basado en Plataformas.

### Integrantes 
* Josue Torres
* Alexis Roman

---

## Tecnologías y Herramientas

El desarrollo del frontend se basa en las siguientes tecnologías:

* **Framework:** SvelteKit (Enrutamiento basado en archivos).
* **Estilos:** TailwindCSS.
* **Gestión de Estado:** Svelte Stores (Autenticación y Persistencia).
* **Cliente HTTP:** Axios (Configurado con interceptores para JWT).
* **Entorno:** Node.js & Docker.

---

## Estructura del Directorio

La organización del código fuente sigue una arquitectura modular, separando la lógica de la API, componentes visuales y la gestión de estado global.

```
frontend/
├── src/
│   ├── lib/
[cite_start]│   │   ├── api/              # Capa de servicios para consumo de API [cite: 210]
[cite_start]│   │   │   ├── axios.js      # Configuración de Axios e interceptores [cite: 211]
[cite_start]│   │   │   ├── auth.js       # Endpoints de autenticación [cite: 249]
[cite_start]│   │   │   ├── users.js      # Endpoints de usuarios [cite: 250]
[cite_start]│   │   │   └── attendance.js # Endpoints de asistencia [cite: 251]
│   │   │
[cite_start]│   │   ├── components/       # Componentes UI reutilizables [cite: 255]
[cite_start]│   │   │   ├── Sidebar.svelte # Navegación lateral [cite: 256]
│   │   │   ├── Navbar.svelte  # Barra superior
[cite_start]│   │   │   ├── Table.svelte   # Tablas de datos estandarizadas [cite: 258]
[cite_start]│   │   │   └── Modal.svelte   # Ventanas emergentes para formularios [cite: 260]
│   │   │
[cite_start]│   │   └── stores/           # Gestión de estado global [cite: 262]
[cite_start]│   │       └── auth.js       # Store de sesión (Login/Logout/Token) [cite: 249]
│   │
[cite_start]│   └── routes/               # Páginas y Rutas del sistema [cite: 24]
[cite_start]│       ├── login/            # Inicio de sesión [cite: 37]
[cite_start]│       ├── dashboard/        # Panel principal [cite: 110]
[cite_start]│       ├── empleados/        # Gestión CRUD de empleados 
[cite_start]│       ├── asistencia/       # Registro y reporte de asistencia [cite: 144]
[cite_start]│       ├── horarios/         # Gestión de horarios [cite: 156]
[cite_start]│       ├── nomina/           # Roles de pago [cite: 175]
[cite_start]│       └── reportes/         # Estadísticas del sistema [cite: 189]
└── package.json
```
## Pasos para la ejecucion

**1. Clonar el Repositorio:**  
```git clone [https://github.com/vinirmn007/GestionEmpleados](https://github.com/vinirmn007/GestionEmpleados)```  
**2. Ejecutar el Backend:**  
Dirigirse al directorio del backend: ```cd backend```  
Levantar los contenedores: ```cd backend```  
**2. Ejecutar el Frontend:**  
Dirigirse al directorio del frontend: ```cd frontend```  
Instalar dependencias: ```npm install```  
Ejecutar: ```npm run dev```
