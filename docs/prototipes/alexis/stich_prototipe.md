# HR SYSTEM PRO - MAPA DE NAVEGACIÓN Y DOCUMENTACIÓN UI

Este documento describe el flujo de usuario, la estructura de navegación y el detalle de las interfaces de usuario (UI) implementadas en el sistema HR System Pro.

---

## 1. Autenticación

### Login / Inicio de Sesión
**Propósito:** Permitir el acceso seguro de los administradores y usuarios autorizados a la plataforma.

**Componentes Principales:**
* **Formulario:** Campos de entrada para "Usuario/Email" y "Contraseña".
* **Botón de Acción:** "Acceder" (Redirige al Dashboard).
* **Recuperación:** Enlace "¿Olvidaste tu contraseña?".

![Inicio de Sesión](/docs/prototypes/alexis/light/inicioSesion.jpg)

---

## 2. Módulo de Empleados

### Dashboard de Empleados
**Propósito:** Vista principal que permite visualizar, filtrar y gestionar el listado de todos los colaboradores de la empresa.

**Componentes Principales:**
* **Barra de Búsqueda:** Búsqueda por nombre o ID.
* **Filtros:** Dropdowns para Departamento, Puesto y Estado.
* **Tabla de Datos:** Muestra foto, nombre, ID, departamento, puesto y estado (Activo/Inactivo).
* **Botón Primario:** "Añadir Nuevo Empleado" (Navega al formulario de registro).

![Dashboard de Empleados](/docs/prototypes/alexis/light/dashboardEmpleados.png)

### Registro de Nuevo Empleado
**Propósito:** Formulario para dar de alta a un nuevo colaborador en el sistema.

**Componentes Principales:**
* **Campos de Texto:** Nombre, Apellido, DNI/Documento de Identidad.
* **Selector:** Posición / Cargo.
* **Botón de Acción:** "Registrar Empleado" (Guarda los datos).

![Registro de Empleados](/docs/prototypes/alexis/light/registroEmpleados.png)

---

## 3. Módulo de Nómina (Roles de Pago)

### Gestión de Roles de Pago (Historial)
**Propósito:** Visualizar el historial de los roles de pago generados anteriormente y su estado.

**Componentes Principales:**
* **Filtros de Período:** Selectores de Mes y Año.
* **Tabla de Resumen:** Muestra período, fecha de generación, n.º empleados, monto total y estado (Pagado/Pendiente).
* **Botón Primario:** "Generar Nuevo Rol de Pago".
* **Acciones de Fila:** Ver detalles, descargar o eliminar.

![Gestión de Roles](/docs/prototypes/alexis/light/creacionRoles.png)

### Creación de Rol de Pago (Paso 1)
**Propósito:** Iniciar el proceso de cálculo de nómina seleccionando el período temporal específico.

**Componentes Principales:**
* **Selector de Fecha:** Input tipo calendario para elegir Mes/Año.
* **Botón de Acción:** "Generar Roles de Pago" (Procesa los cálculos y lleva al detalle).

![Creación de Rol](/docs/prototypes/alexis/light/creacionRol.png)

### Detalle de Roles de Pago (Paso 2)
**Propósito:** Revisar los montos calculados (ingresos y deducciones) por empleado antes de finalizar el proceso.

**Componentes Principales:**
* **Filtros:** Período, Departamento y Estado.
* **Tabla Detallada:** Muestra Empleado, Sueldo Bruto, Deducciones, Sueldo Neto.
* **Indicadores de Estado:** Etiquetas (Pendiente, Pagado, Error).
* **Botón Final:** "Enviar al Gestor de Pagos".

![Detalle de Roles](/docs/prototypes/alexis/light/detalleRoles.png)

### Configuración de Nómina
**Propósito:** Definir las variables globales monetarias que afectan el cálculo de los sueldos.

**Componentes Principales:**
* **Inputs Numéricos (Por Hora):** Pago Hora Normal, Hora Extra, Hora Nocturna.
* **Inputs Numéricos (Otros):** Multa por atraso (minuto), Deducción por ausencia, Bonificaciones.
* **Botonera:** Cancelar / Guardar Cambios.

![Editar Nómina](/docs/prototypes/alexis/light/editarNomina.png)

---

## 4. Módulo de Asistencia

### Gestión de Marcaciones
**Propósito:** Supervisar y corregir el registro diario de entradas y salidas del personal.

**Componentes Principales:**
* **Buscador y Filtros:** Por empleado, fecha, departamento y estado.
* **Tabla de Asistencia:** Hora Entrada, Hora Salida, Horas trabajadas.
* **Alertas:** Etiquetas de estado (Completo, Incompleto, Editado).
* **Acciones:** Icono de chat/edición para justificaciones.

![Editar Marcaciones](/docs/prototypes/alexis/light/editarMarcaciones.png)

---

## 5. Módulo de Horarios

### Gestión de Horarios
**Propósito:** Planificar y visualizar los turnos de trabajo asignados semanal o mensualmente.

**Componentes Principales:**
* **Navegación Temporal:** Selector de semana/mes.
* **Vista Calendario/Tabla:** Filas por empleado y columnas por día de la semana.
* **Bloques de Turno:** Indicadores visuales con horas y tipo de turno (Mañana, Tarde, Noche).
* **Botón Primario:** "Añadir Turno".
* **Barra de Acción Flotante:** Descartar / Guardar Horario.

![Gestión de Horarios](/docs/prototypes/alexis/light/gestionHorarios.png)

---

## 6. Módulo de Permisos

### Gestión de Permisos
**Propósito:** Administrar las solicitudes de vacaciones, permisos por enfermedad o asuntos personales.

**Componentes Principales:**
* **Filtros de Estado:** Tabs (Todos, Pendiente, Aprobado, Denegado).
* **Lista de Solicitudes:** Tarjetas o filas con el empleado, motivo y fechas.
* **Área de Decisión:** Caja de texto para "Motivo de la Decisión" (opcional).
* **Botones de Acción:** "Aprobar" (Verde) y "Denegar" (Rojo).

![Gestión de Permisos](/docs/prototypes/alexis/light/gestionPermisos.png)

---

## Comportamiento Responsivo

* **Escritorio (> 768px):** El menú lateral (Sidebar) permanece fijo y visible. Las tablas muestran la información completa en columnas.
* **Móvil (< 768px):** El menú lateral se oculta y es accesible mediante un botón "hamburguesa". Las tablas de datos se transforman en tarjetas verticales para facilitar la lectura, ocultando detalles secundarios tras un botón de "Expandir".