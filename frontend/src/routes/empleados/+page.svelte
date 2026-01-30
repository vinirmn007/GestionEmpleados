<script>
    import { onMount } from "svelte";
    import api from "$lib/utils/api";
    // Agregamos AlertTriangle para el modal de advertencia
    import {
        Search,
        Plus,
        Pencil,
        Trash2,
        MapPin,
        AlertTriangle,
        X,
        Save,
        Loader2,
    } from "lucide-svelte";

    let empleados = [];
    let search = "";

    // Variables para el control del Modal
    let showDeleteModal = false;
    let employeeToDelete = null;

    let statusesMap = {};

    async function loadEmpleados() {
        try {
            // Cargar empleados y status en paralelo
            const [usersResponse, statusesResponse] = await Promise.all([
                api.get("/usuarios/list"),
                api.get("/nomina/statuses"),
            ]);

            const users = usersResponse.data.data;
            const statuses = statusesResponse.data;

            // Crear mapa de statuses: ID -> Nombre
            statusesMap = statuses.reduce((acc, status) => {
                acc[status.id] = status.name;
                return acc;
            }, {});

            empleados = users;
        } catch (e) {
            console.error("Error cargando datos", e);
            // Datos dummy para visualización en caso de error
            empleados = [
                {
                    id: "EMP-001",
                    nombre: "Ana García Pérez",
                    correo: "ana@example.com",
                    dept: "Tecnología",
                    status: "Activo",
                    direccion: "Av. Universitaria 123",
                    job_status_id: 1,
                },
                {
                    id: "EMP-002",
                    nombre: "Carlos Ruiz",
                    correo: "carlos@example.com",
                    dept: "Ventas",
                    status: "Activo",
                    direccion: "Calle Bolívar y Rocafuerte",
                    job_status_id: 2,
                },
            ];
        }
    }

    // Variables para el control del Modal de Edición
    let showEditModal = false;
    let updating = false;
    let currentEmployee = {
        id: "",
        nombre: "",
        correo: "",
        celular: "",
        direccion: "",
        rol: "empleado",
        activo: true,
        job_status_id: null,
    };

    function handleEdit(id) {
        const emp = empleados.find((e) => e.id === id);
        if (emp) {
            currentEmployee = { ...emp };
            showEditModal = true;
        }
    }

    function closeEditModal() {
        showEditModal = false;
        currentEmployee = {
            id: "",
            nombre: "",
            correo: "",
            celular: "",
            direccion: "",
            rol: "empleado",
            activo: true,
            job_status_id: null,
        };
    }

    async function saveEmployee() {
        updating = true;
        try {
            const payload = {
                nombre: currentEmployee.nombre,
                correo: currentEmployee.correo,
                celular: currentEmployee.celular,
                direccion: currentEmployee.direccion,
                rol: currentEmployee.rol,
                activo: currentEmployee.activo,
                job_status_id: currentEmployee.job_status_id,
            };

            await api.put(`/usuarios/update/${currentEmployee.id}`, payload);
            await loadEmpleados();
            closeEditModal();
        } catch (e) {
            console.error("Error actualizando empleado", e);
            alert(
                "Error al actualizar: " +
                    (e.response?.data?.detail || e.message),
            );
        } finally {
            updating = false;
        }
    }

    // Paso 1: Abrir el modal y guardar el ID
    function openDeleteModal(id) {
        employeeToDelete = id;
        showDeleteModal = true;
    }

    // Paso 2: Cerrar modal y limpiar estado
    function closeDeleteModal() {
        showDeleteModal = false;
        employeeToDelete = null;
    }

    // Paso 3: Ejecutar la eliminación real
    async function confirmDelete() {
        if (!employeeToDelete) return;

        try {
            await api.delete(`/usuarios/delete/${employeeToDelete}`);
            empleados = empleados.filter((emp) => emp.id !== employeeToDelete);
            console.log("Empleado eliminado:", employeeToDelete);
        } catch (e) {
            console.error("Error eliminando empleado", e);
        } finally {
            closeDeleteModal();
        }
    }

    onMount(loadEmpleados);
</script>

{#if showEditModal}
    <div
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4"
    >
        <div
            class="w-full max-w-2xl rounded-xl bg-white p-6 shadow-xl dark:bg-gray-800 overflow-y-auto max-h-[90vh]"
        >
            <div class="mb-4 flex items-center justify-between">
                <h3 class="text-lg font-bold text-gray-900 dark:text-white">
                    Editar Empleado
                </h3>
                <button
                    on:click={closeEditModal}
                    class="text-gray-500 hover:text-gray-700"
                >
                    <X size={20} />
                </button>
            </div>

            <form
                on:submit|preventDefault={saveEmployee}
                class="grid grid-cols-1 gap-4 sm:grid-cols-2"
            >
                <!-- Nombre -->
                <div class="col-span-1 sm:col-span-2">
                    <label
                        class="mb-1 block text-sm font-medium text-gray-700 dark:text-gray-300"
                        >Nombre Completo</label
                    >
                    <input
                        type="text"
                        bind:value={currentEmployee.nombre}
                        required
                        class="block w-full rounded-lg border border-gray-300 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                    />
                </div>

                <!-- Correo -->
                <div>
                    <label
                        class="mb-1 block text-sm font-medium text-gray-700 dark:text-gray-300"
                        >Correo Electrónico</label
                    >
                    <input
                        type="email"
                        bind:value={currentEmployee.correo}
                        required
                        class="block w-full rounded-lg border border-gray-300 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                    />
                </div>

                <!-- Celular -->
                <div>
                    <label
                        class="mb-1 block text-sm font-medium text-gray-700 dark:text-gray-300"
                        >Celular</label
                    >
                    <input
                        type="text"
                        bind:value={currentEmployee.celular}
                        required
                        class="block w-full rounded-lg border border-gray-300 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                    />
                </div>

                <!-- Dirección -->
                <div class="col-span-1 sm:col-span-2">
                    <label
                        class="mb-1 block text-sm font-medium text-gray-700 dark:text-gray-300"
                        >Dirección</label
                    >
                    <input
                        type="text"
                        bind:value={currentEmployee.direccion}
                        required
                        class="block w-full rounded-lg border border-gray-300 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                    />
                </div>

                <!-- Rol -->
                <div>
                    <label
                        class="mb-1 block text-sm font-medium text-gray-700 dark:text-gray-300"
                        >Rol Sistema</label
                    >
                    <select
                        bind:value={currentEmployee.rol}
                        class="block w-full rounded-lg border border-gray-300 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                    >
                        <option value="empleado">Empleado</option>
                        <option value="gerente">Gerente</option>
                    </select>
                </div>

                <!-- Status / Cargo (Dinámico) -->
                <div>
                    <label
                        class="mb-1 block text-sm font-medium text-gray-700 dark:text-gray-300"
                        >Cargo / Status</label
                    >
                    <select
                        bind:value={currentEmployee.job_status_id}
                        class="block w-full rounded-lg border border-gray-300 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                    >
                        <option value={null}>-- Seleccionar --</option>
                        {#each Object.entries(statusesMap) as [id, name]}
                            <!-- La llave del mapa es string, el valor id en DB es int, hacemos cast -->
                            <option value={Number(id)}>{name}</option>
                        {/each}
                    </select>
                </div>

                <!-- Activo/Inactivo -->
                <div class="flex items-center gap-2 mt-4">
                    <input
                        type="checkbox"
                        bind:checked={currentEmployee.activo}
                        id="activeCheck"
                        class="w-4 h-4 text-blue-600 rounded border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800"
                    />
                    <label
                        for="activeCheck"
                        class="ml-2 text-sm font-medium text-gray-900 dark:text-gray-300"
                        >Usuario Activo</label
                    >
                </div>

                <div
                    class="col-span-1 sm:col-span-2 mt-4 flex justify-end gap-3 border-t border-gray-100 pt-4 dark:border-gray-700"
                >
                    <button
                        type="button"
                        on:click={closeEditModal}
                        class="rounded-lg border border-gray-300 px-4 py-2 text-sm font-medium hover:bg-gray-50 dark:border-gray-600 dark:text-white dark:hover:bg-gray-700"
                    >
                        Cancelar
                    </button>
                    <button
                        type="submit"
                        disabled={updating}
                        class="flex items-center gap-2 rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-50"
                    >
                        {#if updating}
                            <Loader2 class="animate-spin" size={16} />
                        {/if}
                        <Save size={16} />
                        Guardar Cambios
                    </button>
                </div>
            </form>
        </div>
    </div>
{/if}

{#if showDeleteModal}
    <div class="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-0">
        <div
            class="absolute inset-0 bg-gray-900/50 dark:bg-black/60 backdrop-blur-sm transition-opacity"
            on:click={closeDeleteModal}
            role="button"
            tabindex="0"
            on:keydown={(e) => e.key === "Escape" && closeDeleteModal()}
        ></div>

        <div
            class="relative w-full max-w-md transform overflow-hidden rounded-xl bg-white dark:bg-gray-800 text-left shadow-2xl transition-all border border-gray-100 dark:border-gray-700"
        >
            <div class="p-6">
                <div
                    class="flex items-center justify-center gap-4 flex-col sm:flex-row sm:items-start"
                >
                    <div
                        class="mx-auto flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-full bg-red-100 dark:bg-red-900/30 sm:mx-0 sm:h-10 sm:w-10"
                    >
                        <AlertTriangle
                            class="h-6 w-6 text-red-600 dark:text-red-400"
                        />
                    </div>

                    <div class="mt-3 text-center sm:ml-4 sm:mt-0 sm:text-left">
                        <h3
                            class="text-lg font-semibold leading-6 text-gray-900 dark:text-white"
                        >
                            Eliminar Empleado
                        </h3>
                        <div class="mt-2">
                            <p class="text-sm text-gray-500 dark:text-gray-400">
                                ¿Estás seguro de que deseas eliminar este
                                registro? Esta acción no se puede deshacer y se
                                perderán los datos asociados.
                            </p>
                        </div>
                    </div>
                </div>
            </div>

            <div
                class="bg-gray-50 dark:bg-gray-800/50 px-6 py-4 sm:flex sm:flex-row-reverse sm:gap-3 border-t border-gray-100 dark:border-gray-700"
            >
                <button
                    type="button"
                    class="inline-flex w-full justify-center rounded-lg bg-red-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-red-500 sm:w-auto transition-colors"
                    on:click={confirmDelete}
                >
                    Sí, eliminar
                </button>
                <button
                    type="button"
                    class="mt-3 inline-flex w-full justify-center rounded-lg bg-white dark:bg-gray-700 px-3 py-2 text-sm font-semibold text-gray-900 dark:text-gray-200 shadow-sm ring-1 ring-inset ring-gray-300 dark:ring-gray-600 hover:bg-gray-50 dark:hover:bg-gray-600 sm:mt-0 sm:w-auto transition-colors"
                    on:click={closeDeleteModal}
                >
                    Cancelar
                </button>
            </div>
        </div>
    </div>
{/if}

<div class="mb-6 flex items-center justify-between">
    <h1 class="text-2xl font-bold text-gray-800 dark:text-white">
        Dashboard de Empleados
    </h1>
    <a
        href="/empleados/nuevo"
        class="flex items-center gap-2 rounded-lg bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 shadow-sm transition-colors"
    >
        <Plus size={20} /> Añadir Nuevo Empleado
    </a>
</div>

<div
    class="rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 p-4 shadow-sm"
>
    <div class="mb-6 flex flex-wrap gap-4">
        <div class="relative flex-1">
            <Search
                class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 dark:text-gray-500"
                size={20}
            />
            <input
                bind:value={search}
                type="text"
                placeholder="Buscar empleados por nombre o ID"
                class="w-full rounded-lg border border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-700 py-2 pl-10 pr-4 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
        </div>
        <select
            class="rounded-lg border border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-700 px-4 py-2 text-gray-600 dark:text-gray-300 focus:ring-2 focus:ring-blue-500 outline-none"
        >
            <option>Departamento</option>
        </select>
        <select
            class="rounded-lg border border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-700 px-4 py-2 text-gray-600 dark:text-gray-300 focus:ring-2 focus:ring-blue-500 outline-none"
        >
            <option>Estado</option>
        </select>
    </div>

    <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse">
            <thead
                class="border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50 text-sm font-semibold text-gray-600 dark:text-gray-400 uppercase tracking-wider"
            >
                <tr>
                    <th class="px-6 py-4">Nombre Completo</th>
                    <th class="px-6 py-4">ID / Correo</th>
                    <th class="px-6 py-4">Dirección</th>
                    <th class="px-6 py-4">Estado</th>
                    <th class="px-6 py-4">Status / Cargo</th>
                    <th class="px-6 py-4 text-center">Acciones</th>
                </tr>
            </thead>
            <tbody class="divide-y divide-gray-100 dark:divide-gray-700">
                {#each empleados as emp}
                    <tr
                        class="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors group"
                    >
                        <td class="px-6 py-4">
                            <div class="flex items-center gap-3">
                                <div
                                    class="h-10 w-10 rounded-full bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center text-white shadow-sm font-bold text-sm"
                                >
                                    {emp.nombre.charAt(0).toUpperCase()}
                                </div>
                                <span
                                    class="font-medium text-gray-900 dark:text-white"
                                    >{emp.nombre}</span
                                >
                            </div>
                        </td>

                        <td class="px-6 py-4">
                            <div class="flex flex-col">
                                <span
                                    class="text-sm font-medium text-gray-700 dark:text-gray-300"
                                    >{emp.id}</span
                                >
                                <span
                                    class="text-xs text-gray-500 dark:text-gray-400"
                                    >{emp.correo}</span
                                >
                            </div>
                        </td>

                        <td
                            class="px-6 py-4 text-gray-600 dark:text-gray-400 text-sm"
                        >
                            <div class="flex items-center gap-2">
                                <MapPin
                                    size={14}
                                    class="text-gray-400 dark:text-gray-500"
                                />
                                <span
                                    class="truncate max-w-[200px]"
                                    title={emp.direccion}
                                >
                                    {emp.direccion ||
                                        "Sin dirección registrada"}
                                </span>
                            </div>
                        </td>

                        <td class="px-6 py-4">
                            {#if emp.status === "Activo"}
                                <span
                                    class="inline-flex items-center rounded-full bg-green-100 dark:bg-green-900/30 px-2.5 py-0.5 text-xs font-medium text-green-800 dark:text-green-400"
                                    >Activo</span
                                >
                            {:else}
                                <span
                                    class="inline-flex items-center rounded-full bg-gray-100 dark:bg-gray-700 px-2.5 py-0.5 text-xs font-medium text-gray-800 dark:text-gray-300"
                                    >Inactivo</span
                                >
                            {/if}
                        </td>

                        <td class="px-6 py-4">
                            <span
                                class="inline-flex items-center rounded-full border border-blue-200 bg-blue-50 dark:bg-blue-900/20 dark:border-blue-800 px-2.5 py-0.5 text-xs font-medium text-blue-800 dark:text-blue-300"
                            >
                                {statusesMap[emp.job_status_id] ||
                                    "No asignado"}
                            </span>
                        </td>

                        <td class="px-6 py-4">
                            <div class="flex items-center justify-center gap-2">
                                <button
                                    on:click={() => handleEdit(emp.id)}
                                    class="p-2 text-blue-600 dark:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/20 rounded-lg transition-colors"
                                    title="Editar"
                                >
                                    <Pencil size={18} />
                                </button>
                                <button
                                    on:click={() => openDeleteModal(emp.id)}
                                    class="p-2 text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-colors"
                                    title="Eliminar"
                                >
                                    <Trash2 size={18} />
                                </button>
                            </div>
                        </td>
                    </tr>
                {/each}
            </tbody>
        </table>
    </div>
</div>
