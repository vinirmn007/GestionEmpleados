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
│   ├── api/              # Capa de servicios para consumo de API 
│   │   ├── axios.js      # Configuración de Axios e interceptores 
│   │   ├── auth.js       # Endpoints de autenticación 
│   │   ├── users.js      # Endpoints de usuarios 
│   │   └── attendance.js # Endpoints de asistencia 
│   │   │
│   ├── components/       # Componentes UI reutilizables 
│   │   ├── Sidebar.svelte # Navegación lateral 
│   │   │   ├── Navbar.svelte  # Barra superior
│   │   ├── Table.svelte   # Tablas de datos estandarizadas 
│   │   └── Modal.svelte   # Ventanas emergentes para formularios 
│   │   │
│   └── stores/           # Gestión de estado global 
│       └── auth.js       # Store de sesión (Login/Logout/Token) 
│   │
└── routes/               # Páginas y Rutas del sistema 
    ├── login/            # Inicio de sesión 
    ├── dashboard/        # Panel principal 
    ├── empleados/        # Gestión CRUD de empleados 
    ├── asistencia/       # Registro y reporte de asistencia 
    ├── horarios/         # Gestión de horarios 
    ├── nomina/           # Roles de pago 
    └── reportes/         # Estadísticas del sistema 
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
