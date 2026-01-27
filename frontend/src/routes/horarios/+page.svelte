<script>
    import { onMount } from "svelte";
    import api from "$lib/utils/api";
    // Agregamos Pencil, AlertTriangle y X
    import { Search, Calendar, Clock, Trash2, Plus, User, Pencil, AlertTriangle, X } from "lucide-svelte";

    let employees = [];
    let selectedEmployee = null;
    let schedules = [];
    let loadingEmployees = false;
    let loadingSchedules = false;
    let searchTerm = "";
    let error = "";

    // --- ESTADOS PARA MODALES ---
    let showDeleteModal = false;
    let scheduleToDelete = null;

    let showEditModal = false;
    let editingSchedule = {
        id: null,
        day_of_week: "",
        start_time: "",
        end_time: ""
    };

    let newSchedule = {
        day_of_week: "Lunes",
        start_time: "09:00",
        end_time: "17:00",
    };

    const daysOfWeek = [
        "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo",
    ];

    // --- CARGA DE DATOS ---
    async function loadEmployees() {
        loadingEmployees = true;
        try {
            const { data } = await api.get("/usuarios/list");
            employees = data.data || [];
        } catch (e) {
            console.error("Error loading employees", e);
            error = "No se pudieron cargar los empleados.";
        } finally {
            loadingEmployees = false;
        }
    }

    async function selectEmployee(employee) {
        selectedEmployee = employee;
        loadSchedules(employee.id);

        if (window.innerWidth < 1024) {
            setTimeout(() => {
                const schedulePanel = document.getElementById("schedule-panel");
                if (schedulePanel)
                    schedulePanel.scrollIntoView({ behavior: "smooth" });
            }, 100);
        }
    }

    async function loadSchedules(userId) {
        loadingSchedules = true;
        schedules = [];
        try {
            const { data } = await api.get(`/horarios/${userId}/schedule`);
            schedules = data;
        } catch (e) {
            console.error("Error loading schedules", e);
            schedules = [];
        } finally {
            loadingSchedules = false;
        }
    }

    // --- LÓGICA DE CREACIÓN ---
    async function addSchedule() {
        if (!selectedEmployee) return;

        try {
            const payload = {
                user_id: selectedEmployee.id,
                day_of_week: newSchedule.day_of_week,
                start_time: newSchedule.start_time,
                end_time: newSchedule.end_time,
            };

            await api.post("/horarios/schedules/assignments", payload);
            await loadSchedules(selectedEmployee.id);
        } catch (e) {
            console.error("Error adding schedule", e);
            alert("Error al asignar horario.");
        }
    }

    // --- LÓGICA DE EDICIÓN ---
    function openEditModal(schedule) {
        // Clonamos el objeto para no editar directamente la referencia en la lista hasta confirmar
        editingSchedule = { ...schedule };
        showEditModal = true;
    }

    function closeEditModal() {
        showEditModal = false;
        editingSchedule = { id: null, day_of_week: "", start_time: "", end_time: "" };
    }

    async function confirmEdit() {
        if (!editingSchedule.id) return;
        
        try {
            // Asumiendo ruta PUT para actualización
            await api.put(`/horarios/schedules/${editingSchedule.id}`, {
                day_of_week: editingSchedule.day_of_week,
                start_time: editingSchedule.start_time,
                end_time: editingSchedule.end_time
            });
            
            await loadSchedules(selectedEmployee.id);
            closeEditModal();
        } catch (e) {
            console.error("Error updating schedule", e);
            alert("Error al actualizar el horario");
        }
    }

    // --- LÓGICA DE ELIMINACIÓN ---
    function openDeleteModal(id) {
        scheduleToDelete = id;
        showDeleteModal = true;
    }

    function closeDeleteModal() {
        showDeleteModal = false;
        scheduleToDelete = null;
    }

    async function confirmDelete() {
        if (!scheduleToDelete) return;

        try {
            await api.delete(`/horarios/schedules/${scheduleToDelete}`);
            await loadSchedules(selectedEmployee.id);
        } catch (e) {
            console.error("Error deleting schedule", e);
            alert("Error al eliminar el horario.");
        } finally {
            closeDeleteModal();
        }
    }

    onMount(() => {
        loadEmployees();
    });

    $: filteredEmployees = employees.filter(
        (e) =>
            e.nombre.toLowerCase().includes(searchTerm.toLowerCase()) ||
            e.email.toLowerCase().includes(searchTerm.toLowerCase()),
    );
</script>

{#if showDeleteModal}
    <div class="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-0">
        <div 
            class="absolute inset-0 bg-gray-900/50 dark:bg-black/60 backdrop-blur-sm transition-opacity"
            on:click={closeDeleteModal} 
            role="button" 
            tabindex="0"
            on:keydown={(e) => e.key === 'Escape' && closeDeleteModal()}
        ></div>

        <div class="relative w-full max-w-md transform overflow-hidden rounded-xl bg-white dark:bg-gray-800 text-left shadow-2xl transition-all border border-gray-100 dark:border-gray-700">
            <div class="p-6">
                <div class="flex items-center justify-center gap-4 flex-col sm:flex-row sm:items-start">
                    <div class="mx-auto flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-full bg-red-100 dark:bg-red-900/30 sm:mx-0 sm:h-10 sm:w-10">
                        <AlertTriangle class="h-6 w-6 text-red-600 dark:text-red-400" />
                    </div>
                    <div class="mt-3 text-center sm:ml-4 sm:mt-0 sm:text-left">
                        <h3 class="text-lg font-semibold leading-6 text-gray-900 dark:text-white">
                            Eliminar Horario
                        </h3>
                        <div class="mt-2">
                            <p class="text-sm text-gray-500 dark:text-gray-400">
                                ¿Estás seguro de que deseas eliminar este horario asignado? Esta acción no se puede deshacer.
                            </p>
                        </div>
                    </div>
                </div>
            </div>
            <div class="bg-gray-50 dark:bg-gray-800/50 px-6 py-4 sm:flex sm:flex-row-reverse sm:gap-3 border-t border-gray-100 dark:border-gray-700">
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

{#if showEditModal}
    <div class="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-0">
        <div 
            class="absolute inset-0 bg-gray-900/50 dark:bg-black/60 backdrop-blur-sm transition-opacity"
            on:click={closeEditModal} 
            role="button" 
            tabindex="0"
            on:keydown={(e) => e.key === 'Escape' && closeEditModal()}
        ></div>

        <div class="relative w-full max-w-lg transform overflow-hidden rounded-xl bg-white dark:bg-gray-800 text-left shadow-2xl transition-all border border-gray-100 dark:border-gray-700">
            <div class="flex items-center justify-between px-6 py-4 border-b border-gray-100 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50">
                <h3 class="text-lg font-semibold text-gray-900 dark:text-white flex items-center gap-2">
                    <Clock size={20} class="text-blue-600 dark:text-blue-400" />
                    Editar Horario
                </h3>
                <button on:click={closeEditModal} class="text-gray-400 hover:text-gray-500 dark:hover:text-gray-300">
                    <X size={20} />
                </button>
            </div>

            <div class="p-6 space-y-4">
                <div>
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Día de la semana</label>
                    <select
                        bind:value={editingSchedule.day_of_week}
                        class="w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 py-2 px-3 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 outline-none"
                    >
                        {#each daysOfWeek as day}
                            <option value={day}>{day}</option>
                        {/each}
                    </select>
                </div>
                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Hora Entrada</label>
                        <input
                            type="time"
                            bind:value={editingSchedule.start_time}
                            class="w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 py-2 px-3 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 outline-none"
                        />
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Hora Salida</label>
                        <input
                            type="time"
                            bind:value={editingSchedule.end_time}
                            class="w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 py-2 px-3 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 outline-none"
                        />
                    </div>
                </div>
            </div>

            <div class="px-6 py-4 bg-gray-50 dark:bg-gray-800/50 border-t border-gray-100 dark:border-gray-700 flex justify-end gap-3">
                <button
                    type="button"
                    class="rounded-lg bg-white dark:bg-gray-700 px-4 py-2 text-sm font-semibold text-gray-700 dark:text-gray-200 shadow-sm ring-1 ring-inset ring-gray-300 dark:ring-gray-600 hover:bg-gray-50 dark:hover:bg-gray-600 transition-colors"
                    on:click={closeEditModal}
                >
                    Cancelar
                </button>
                <button
                    type="button"
                    class="rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-blue-500 transition-colors"
                    on:click={confirmEdit}
                >
                    Guardar Cambios
                </button>
            </div>
        </div>
    </div>
{/if}

<div class="flex flex-col lg:flex-row lg:h-[calc(100vh-100px)] gap-6 pb-10 lg:pb-0">
    <div class="w-full lg:w-1/3 h-80 lg:h-full flex flex-col rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 shadow-sm overflow-hidden shrink-0">
        <div class="p-4 border-b border-gray-100 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50">
            <h2 class="text-lg font-semibold text-gray-800 dark:text-white mb-3">
                Empleados
            </h2>
            <div class="relative">
                <Search class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 dark:text-gray-500" size={18} />
                <input
                    bind:value={searchTerm}
                    type="text"
                    placeholder="Buscar..."
                    class="w-full rounded-lg border border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-700 py-2 pl-10 pr-4 text-sm text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
            </div>
        </div>

        <div class="flex-1 overflow-y-auto p-2 space-y-1">
            {#if loadingEmployees}
                <div class="p-4 text-center text-gray-500 dark:text-gray-400">Cargando empleados...</div>
            {:else if filteredEmployees.length === 0}
                <div class="p-4 text-center text-gray-500 dark:text-gray-400">No se encontraron empleados.</div>
            {:else}
                {#each filteredEmployees as emp}
                    <button
                        class="w-full flex items-center gap-3 p-3 rounded-lg transition-colors text-left
                        {selectedEmployee?.id === emp.id
                            ? 'bg-blue-50 dark:bg-blue-900/30 border-blue-200 dark:border-blue-700 ring-1 ring-blue-200 dark:ring-blue-700'
                            : 'hover:bg-gray-50 dark:hover:bg-gray-700'}"
                        on:click={() => selectEmployee(emp)}
                    >
                        <div class="h-10 w-10 min-w-[2.5rem] rounded-full bg-gray-200 dark:bg-gray-600 flex items-center justify-center text-gray-500 dark:text-gray-300">
                            <User size={20} />
                        </div>
                        <div class="overflow-hidden">
                            <p class="font-medium text-gray-900 dark:text-white truncate">{emp.nombre}</p>
                            <p class="text-xs text-gray-500 dark:text-gray-400 truncate">{emp.email}</p>
                        </div>
                    </button>
                {/each}
            {/if}
        </div>
    </div>

    <div id="schedule-panel" class="w-full lg:flex-1 h-auto lg:h-full flex flex-col rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 shadow-sm overflow-hidden">
        {#if selectedEmployee}
            <div class="p-6 border-b border-gray-100 dark:border-gray-700 flex flex-col sm:flex-row justify-between sm:items-center bg-gray-50 dark:bg-gray-800/50 gap-2">
                <div>
                    <h2 class="text-xl font-bold text-gray-800 dark:text-white">Gestionar Horarios</h2>
                    <p class="text-gray-500 dark:text-gray-400 text-sm">
                        Para: <span class="font-medium text-gray-900 dark:text-white">{selectedEmployee.nombre}</span>
                    </p>
                </div>
                <div class="text-sm text-gray-400 dark:text-gray-500 bg-white dark:bg-gray-700 px-2 py-1 rounded border border-gray-200 dark:border-gray-600 w-fit">
                    ID: {selectedEmployee.id}
                </div>
            </div>

            <div class="p-6 flex-1 lg:overflow-y-auto">
                <div class="mb-8 bg-blue-50/50 dark:bg-blue-900/20 p-4 rounded-xl border border-blue-100 dark:border-blue-800">
                    <h3 class="text-sm font-semibold text-blue-900 dark:text-blue-300 mb-3 flex items-center gap-2">
                        <Plus size={16} /> Asignar Nuevo Horario
                    </h3>

                    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 items-end">
                        <div class="col-span-1 sm:col-span-2 lg:col-span-1">
                            <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">Día</label>
                            <select
                                bind:value={newSchedule.day_of_week}
                                class="w-full rounded-lg border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-700 text-sm py-2 px-3 text-gray-900 dark:text-white focus:ring-blue-500 focus:border-blue-500"
                            >
                                {#each daysOfWeek as day}
                                    <option value={day}>{day}</option>
                                {/each}
                            </select>
                        </div>
                        <div>
                            <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">Entrada</label>
                            <input
                                type="time"
                                bind:value={newSchedule.start_time}
                                class="w-full rounded-lg border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-700 text-sm py-2 px-3 text-gray-900 dark:text-white focus:ring-blue-500 focus:border-blue-500"
                            />
                        </div>
                        <div>
                            <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">Salida</label>
                            <input
                                type="time"
                                bind:value={newSchedule.end_time}
                                class="w-full rounded-lg border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-700 text-sm py-2 px-3 text-gray-900 dark:text-white focus:ring-blue-500 focus:border-blue-500"
                            />
                        </div>
                        <button
                            on:click={addSchedule}
                            class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors flex items-center justify-center gap-2 h-[38px]"
                        >
                            Asignar
                        </button>
                    </div>
                </div>

                <h3 class="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-4 flex items-center gap-2">
                    <Calendar size={16} /> Horarios Asignados
                </h3>

                {#if loadingSchedules}
                    <div class="text-center py-8 text-gray-500 dark:text-gray-400">Cargando horarios...</div>
                {:else if schedules.length === 0}
                    <div class="text-center py-8 bg-gray-50 dark:bg-gray-700/50 rounded-lg border border-dashed border-gray-200 dark:border-gray-600">
                        <p class="text-gray-500 dark:text-gray-400 text-sm">No hay horarios asignados para este empleado.</p>
                    </div>
                {:else}
                    <div class="grid gap-3 sm:grid-cols-2 lg:grid-cols-1">
                        {#each schedules as schedule}
                            <div class="flex items-center justify-between p-4 rounded-lg border border-gray-100 dark:border-gray-700 bg-white dark:bg-gray-800 hover:shadow-sm transition-shadow">
                                <div class="flex items-center gap-4">
                                    <div class="h-10 w-10 rounded-lg bg-indigo-50 dark:bg-indigo-900/30 flex items-center justify-center text-indigo-600 dark:text-indigo-400 font-bold text-xs uppercase shrink-0">
                                        {schedule.day_of_week.substring(0, 3)}
                                    </div>
                                    <div>
                                        <p class="font-medium text-gray-900 dark:text-white">{schedule.day_of_week}</p>
                                        <p class="text-sm text-gray-500 dark:text-gray-400 flex items-center gap-1">
                                            <Clock size={14} />
                                            {schedule.start_time} - {schedule.end_time}
                                        </p>
                                    </div>
                                </div>
                                <div class="flex items-center gap-1">
                                    <button
                                        on:click={() => openEditModal(schedule)}
                                        class="p-2 text-blue-600 dark:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/20 rounded-lg transition-colors"
                                        title="Editar horario"
                                    >
                                        <Pencil size={18} />
                                    </button>
                                    <button
                                        on:click={() => openDeleteModal(schedule.id)}
                                        class="p-2 text-gray-400 dark:text-gray-500 hover:text-red-600 dark:hover:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-colors"
                                        title="Eliminar horario"
                                    >
                                        <Trash2 size={18} />
                                    </button>
                                </div>
                            </div>
                        {/each}
                    </div>
                {/if}
            </div>
        {:else}
             <div class="flex-1 flex flex-col items-center justify-center text-gray-400 dark:text-gray-500 p-8 min-h-[300px]">
                <div class="h-16 w-16 bg-gray-100 dark:bg-gray-700 rounded-full flex items-center justify-center mb-4">
                    <User size={32} />
                </div>
                <p class="text-lg font-medium text-gray-500 dark:text-gray-400">Selecciona un empleado</p>
                <p class="text-sm text-center">Elige un empleado de la lista superior para gestionar sus horarios.</p>
            </div>
        {/if}
    </div>
</div>