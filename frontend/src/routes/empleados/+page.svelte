<script>
    import { onMount } from "svelte";
    import api from "$lib/utils/api";
    // Agregamos iconos necesarios: X, Save, Loader2, User
    import { Search, Plus, Pencil, Trash2, MapPin, AlertTriangle, X, Save, Loader2, User } from "lucide-svelte";

    let empleados = [];
    let search = "";
    
    // --- ESTADO: ELIMINACIÓN ---
    let showDeleteModal = false;
    let employeeToDelete = null;

    // --- ESTADO: EDICIÓN ---
    let showEditModal = false;
    let isSaving = false;
    let editError = "";
    // Objeto temporal para el formulario de edición
    let editForm = {
        id: "",
        nombre: "",
        dni: "", // Solo lectura
        correo: "",
        celular: "",
        direccion: ""
    };

    // --- CARGA DE DATOS ---
    async function loadEmpleados() {
        try {
            const { data } = await api.get("/usuarios/list");
            empleados = data.data;
        } catch (e) {
            console.error("Error cargando empleados", e);
            // Datos dummy
            empleados = [
                {
                    id: "EMP-001",
                    nombre: "Ana García Pérez",
                    dni: "1104517915",
                    correo: "ana@example.com",
                    celular: "0991234567",
                    dept: "Tecnología",
                    status: "Activo",
                    direccion: "Av. Universitaria 123",
                },
                {
                    id: "EMP-002",
                    nombre: "Carlos Ruiz",
                    dni: "1102345678",
                    correo: "carlos@example.com",
                    celular: "0987654321",
                    dept: "Ventas",
                    status: "Activo",
                    direccion: "Calle Bolívar y Rocafuerte",
                }
            ];
        }
    }

    // --- LÓGICA DE EDICIÓN ---
    function openEditModal(emp) {
        // Copiamos los datos al formulario temporal para no mutar la tabla directamente
        editForm = { 
            id: emp.id,
            nombre: emp.nombre,
            dni: emp.dni || "N/A", // Si no viene del backend, poner default
            correo: emp.correo,
            celular: emp.celular || "",
            direccion: emp.direccion || ""
        };
        editError = "";
        showEditModal = true;
    }

    function closeEditModal() {
        showEditModal = false;
        editForm = { id: "", nombre: "", dni: "", correo: "", celular: "", direccion: "" };
    }

    async function handleUpdate() {
        isSaving = true;
        editError = "";

        try {
            // Enviamos solo los campos editables. DNI y Password quedan fuera.
            const payload = {
                nombre: editForm.nombre,
                correo: editForm.correo,
                celular: editForm.celular,
                direccion: editForm.direccion
            };

            // Ajusta la ruta según tu API real (ej: PUT /usuarios/update/:id)
            await api.put(`/usuarios/update/${editForm.id}`, payload);

            // Actualizamos la lista localmente para reflejar cambios sin recargar
            empleados = empleados.map(emp => 
                emp.id === editForm.id ? { ...emp, ...payload } : emp
            );

            closeEditModal();
        } catch (e) {
            console.error("Error al actualizar:", e);
            if (e.response && e.response.data && e.response.data.detail) {
                editError = e.response.data.detail;
            } else {
                editError = "Error al actualizar el empleado.";
            }
        } finally {
            isSaving = false;
        }
    }

    // --- LÓGICA DE ELIMINACIÓN ---
    function openDeleteModal(id) {
        employeeToDelete = id;
        showDeleteModal = true;
    }

    function closeDeleteModal() {
        showDeleteModal = false;
        employeeToDelete = null;
    }

    async function confirmDelete() {
        if (!employeeToDelete) return;
        try {
            await api.delete(`/usuarios/delete/${employeeToDelete}`);
            empleados = empleados.filter((emp) => emp.id !== employeeToDelete);
        } catch (e) {
            console.error("Error eliminando empleado", e);
        } finally {
            closeDeleteModal();
        }
    }

    onMount(loadEmpleados);
</script>

{#if showDeleteModal}
    <div class="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-0">
        <div 
            class="absolute inset-0 bg-gray-900/50 dark:bg-black/60 backdrop-blur-sm transition-opacity"
            on:click={closeDeleteModal} 
            role="button" tabindex="0" on:keydown={(e) => e.key === 'Escape' && closeDeleteModal()}
        ></div>

        <div class="relative w-full max-w-md transform overflow-hidden rounded-xl bg-white dark:bg-gray-800 text-left shadow-2xl transition-all border border-gray-100 dark:border-gray-700">
            <div class="p-6">
                <div class="flex items-center justify-center gap-4 flex-col sm:flex-row sm:items-start">
                    <div class="mx-auto flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-full bg-red-100 dark:bg-red-900/30 sm:mx-0 sm:h-10 sm:w-10">
                        <AlertTriangle class="h-6 w-6 text-red-600 dark:text-red-400" />
                    </div>
                    <div class="mt-3 text-center sm:ml-4 sm:mt-0 sm:text-left">
                        <h3 class="text-lg font-semibold leading-6 text-gray-900 dark:text-white">Eliminar Empleado</h3>
                        <div class="mt-2">
                            <p class="text-sm text-gray-500 dark:text-gray-400">
                                ¿Estás seguro de que deseas eliminar este registro? Esta acción no se puede deshacer.
                            </p>
                        </div>
                    </div>
                </div>
            </div>
            <div class="bg-gray-50 dark:bg-gray-800/50 px-6 py-4 sm:flex sm:flex-row-reverse sm:gap-3 border-t border-gray-100 dark:border-gray-700">
                <button type="button" class="inline-flex w-full justify-center rounded-lg bg-red-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-red-500 sm:w-auto transition-colors" on:click={confirmDelete}>
                    Sí, eliminar
                </button>
                <button type="button" class="mt-3 inline-flex w-full justify-center rounded-lg bg-white dark:bg-gray-700 px-3 py-2 text-sm font-semibold text-gray-900 dark:text-gray-200 shadow-sm ring-1 ring-inset ring-gray-300 dark:ring-gray-600 hover:bg-gray-50 dark:hover:bg-gray-600 sm:mt-0 sm:w-auto transition-colors" on:click={closeDeleteModal}>
                    Cancelar
                </button>
            </div>
        </div>
    </div>
{/if}

{#if showEditModal}
    <div class="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-0">
        <div 
            class="absolute inset-0 bg-gray-900/50 dark:bg-black/60 backdrop-blur-sm transition-opacity"
            on:click={closeEditModal} 
            role="button" tabindex="0" on:keydown={(e) => e.key === 'Escape' && closeEditModal()}
        ></div>

        <div class="relative w-full max-w-2xl transform overflow-hidden rounded-xl bg-white dark:bg-gray-800 text-left shadow-2xl transition-all border border-gray-100 dark:border-gray-700 flex flex-col max-h-[90vh]">
            
            <div class="flex items-center justify-between px-6 py-4 border-b border-gray-100 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50">
                <div class="flex items-center gap-3">
                    <div class="p-2 bg-blue-100 dark:bg-blue-900/30 rounded-lg text-blue-600 dark:text-blue-400">
                        <User size={20} />
                    </div>
                    <div>
                        <h3 class="text-lg font-bold text-gray-900 dark:text-white">Editar Empleado</h3>
                        <p class="text-xs text-gray-500 dark:text-gray-400">Actualiza la información del usuario</p>
                    </div>
                </div>
                <button on:click={closeEditModal} class="text-gray-400 hover:text-gray-500 dark:hover:text-gray-300 transition-colors">
                    <X size={20} />
                </button>
            </div>

            <div class="p-6 overflow-y-auto">
                {#if editError}
                    <div class="mb-4 rounded-lg bg-red-50 dark:bg-red-900/20 p-3 text-sm text-red-800 dark:text-red-400 border border-red-200 dark:border-red-800">
                        {editError}
                    </div>
                {/if}

                <form id="editForm" on:submit|preventDefault={handleUpdate}>
                    <div class="grid gap-6 md:grid-cols-2">
                        <div class="col-span-2 md:col-span-1">
                            <label for="edit_nombre" class="mb-2 block text-sm font-medium text-gray-900 dark:text-gray-200">Nombre Completo</label>
                            <input
                                type="text"
                                id="edit_nombre"
                                bind:value={editForm.nombre}
                                required
                                class="block w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 p-2.5 text-gray-900 dark:text-white focus:border-blue-500 focus:ring-blue-500 focus:outline-none"
                            />
                        </div>

                        <div class="col-span-2 md:col-span-1">
                            <label for="edit_dni" class="mb-2 block text-sm font-medium text-gray-900 dark:text-gray-200">
                                DNI / Cédula <span class="text-xs font-normal text-gray-500 ml-1">(No editable)</span>
                            </label>
                            <input
                                type="text"
                                id="edit_dni"
                                value={editForm.dni}
                                disabled
                                class="block w-full rounded-lg border border-gray-200 dark:border-gray-700 bg-gray-100 dark:bg-gray-800/50 p-2.5 text-gray-500 dark:text-gray-400 cursor-not-allowed select-none"
                            />
                        </div>

                        <div class="col-span-2 md:col-span-1">
                            <label for="edit_correo" class="mb-2 block text-sm font-medium text-gray-900 dark:text-gray-200">Correo Electrónico</label>
                            <input
                                type="email"
                                id="edit_correo"
                                bind:value={editForm.correo}
                                required
                                class="block w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 p-2.5 text-gray-900 dark:text-white focus:border-blue-500 focus:ring-blue-500 focus:outline-none"
                            />
                        </div>

                        <div class="col-span-2 md:col-span-1">
                            <label for="edit_celular" class="mb-2 block text-sm font-medium text-gray-900 dark:text-gray-200">Celular</label>
                            <input
                                type="tel"
                                id="edit_celular"
                                bind:value={editForm.celular}
                                required
                                class="block w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 p-2.5 text-gray-900 dark:text-white focus:border-blue-500 focus:ring-blue-500 focus:outline-none"
                            />
                        </div>

                        <div class="col-span-2">
                            <label for="edit_direccion" class="mb-2 block text-sm font-medium text-gray-900 dark:text-gray-200">Dirección Domiciliaria</label>
                            <input
                                type="text"
                                id="edit_direccion"
                                bind:value={editForm.direccion}
                                required
                                class="block w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 p-2.5 text-gray-900 dark:text-white focus:border-blue-500 focus:ring-blue-500 focus:outline-none"
                            />
                        </div>
                        
                        <div class="col-span-2 rounded-lg bg-blue-50 dark:bg-blue-900/10 p-3 flex items-start gap-2">
                             <div class="text-blue-500 mt-0.5"><AlertTriangle size={16}/></div>
                             <p class="text-xs text-blue-800 dark:text-blue-300">
                                 Por seguridad, la contraseña no se puede editar aquí. El usuario debe usar la opción "¿Olvidaste tu contraseña?" en el login o solicitar un reseteo administrativo.
                             </p>
                        </div>
                    </div>
                </form>
            </div>

            <div class="px-6 py-4 bg-gray-50 dark:bg-gray-800/50 border-t border-gray-100 dark:border-gray-700 flex justify-end gap-3">
                <button
                    type="button"
                    class="rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 px-5 py-2.5 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-600 transition-colors"
                    on:click={closeEditModal}
                >
                    Cancelar
                </button>
                <button
                    type="submit"
                    form="editForm"
                    disabled={isSaving}
                    class="flex items-center gap-2 rounded-lg bg-blue-600 px-5 py-2.5 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                    {#if isSaving}
                        <Loader2 class="animate-spin" size={18} />
                        Guardando...
                    {:else}
                        <Save size={18} />
                        Guardar Cambios
                    {/if}
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

<div class="rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 p-4 shadow-sm">
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
        <select class="rounded-lg border border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-700 px-4 py-2 text-gray-600 dark:text-gray-300 focus:ring-2 focus:ring-blue-500 outline-none">
            <option>Departamento</option>
        </select>
        <select class="rounded-lg border border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-700 px-4 py-2 text-gray-600 dark:text-gray-300 focus:ring-2 focus:ring-blue-500 outline-none">
            <option>Estado</option>
        </select>
    </div>

    <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse">
            <thead class="border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50 text-sm font-semibold text-gray-600 dark:text-gray-400 uppercase tracking-wider">
                <tr>
                    <th class="px-6 py-4">Nombre Completo</th>
                    <th class="px-6 py-4">ID / Correo</th>
                    <th class="px-6 py-4">Dirección</th>
                    <th class="px-6 py-4">Estado</th>
                    <th class="px-6 py-4 text-center">Acciones</th>
                </tr>
            </thead>
            <tbody class="divide-y divide-gray-100 dark:divide-gray-700">
                {#each empleados as emp}
                    <tr class="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors group">
                        <td class="px-6 py-4">
                            <div class="flex items-center gap-3">
                                <div class="h-10 w-10 rounded-full bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center text-white shadow-sm font-bold text-sm">
                                    {emp.nombre.charAt(0).toUpperCase()}
                                </div>
                                <span class="font-medium text-gray-900 dark:text-white">{emp.nombre}</span>
                            </div>
                        </td>

                        <td class="px-6 py-4">
                            <div class="flex flex-col">
                                <span class="text-sm font-medium text-gray-700 dark:text-gray-300">{emp.id}</span>
                                <span class="text-xs text-gray-500 dark:text-gray-400">{emp.correo}</span>
                            </div>
                        </td>

                        <td class="px-6 py-4 text-gray-600 dark:text-gray-400 text-sm">
                            <div class="flex items-center gap-2">
                                <MapPin size={14} class="text-gray-400 dark:text-gray-500" />
                                <span class="truncate max-w-[200px]" title={emp.direccion}>
                                    {emp.direccion || "Sin dirección registrada"}
                                </span>
                            </div>
                        </td>

                        <td class="px-6 py-4">
                            {#if emp.status === "Activo"}
                                <span class="inline-flex items-center rounded-full bg-green-100 dark:bg-green-900/30 px-2.5 py-0.5 text-xs font-medium text-green-800 dark:text-green-400">Activo</span>
                            {:else}
                                <span class="inline-flex items-center rounded-full bg-gray-100 dark:bg-gray-700 px-2.5 py-0.5 text-xs font-medium text-gray-800 dark:text-gray-300">Inactivo</span>
                            {/if}
                        </td>

                        <td class="px-6 py-4">
                            <div class="flex items-center justify-center gap-2">
                                <button on:click={() => openEditModal(emp)} class="p-2 text-blue-600 dark:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/20 rounded-lg transition-colors" title="Editar">
                                    <Pencil size={18} />
                                </button>
                                <button on:click={() => openDeleteModal(emp.id)} class="p-2 text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-colors" title="Eliminar">
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