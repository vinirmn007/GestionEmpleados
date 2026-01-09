<script>
    import { onMount } from 'svelte';
    import api from '$lib/utils/api';
    import { Search, Calendar, Clock, Trash2, Plus, User } from 'lucide-svelte';

    let employees = [];
    let selectedEmployee = null;
    let schedules = [];
    let loadingEmployees = false;
    let loadingSchedules = false;
    let searchTerm = '';
    let error = '';

    // Form data for new schedule
    let newSchedule = {
        day_of_week: 'Lunes',
        start_time: '09:00',
        end_time: '17:00'
    };

    const daysOfWeek = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'];

    async function loadEmployees() {
        loadingEmployees = true;
        try {
            const { data } = await api.get('/usuarios/list');
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
    }

    async function loadSchedules(userId) {
        loadingSchedules = true;
        schedules = [];
        try {
            // GET /horarios/{user_id}/schedule
            const { data } = await api.get(`/horarios/${userId}/schedule`);
            schedules = data;
        } catch (e) {
            console.error("Error loading schedules", e);
            // If 404, it might just mean no schedules yet, but the backend throws 404 if user not found in user service?
            // The backend endpoint validates user first.
            schedules = [];
        } finally {
            loadingSchedules = false;
        }
    }

    async function addSchedule() {
        if (!selectedEmployee) return;
        
        try {
            // POST /horarios/schedules/assignments
            const payload = {
                user_id: selectedEmployee.id,
                day_of_week: newSchedule.day_of_week,
                start_time: newSchedule.start_time,
                end_time: newSchedule.end_time
            };
            
            await api.post('/horarios/schedules/assignments', payload);
            
            // Reload schedules
            await loadSchedules(selectedEmployee.id);
            
            // Reset form slightly? Keep day/times for quick entry of next day maybe?
        } catch (e) {
            console.error("Error adding schedule", e);
            alert("Error al asignar horario. Verifique que el usuario exista y los datos sean correctos.");
        }
    }

    async function deleteSchedule(scheduleId) {
        if (!confirm('¿Estás seguro de eliminar este horario?')) return;
        
        try {
            // DELETE /horarios/schedules/{id}
            await api.delete(`/horarios/schedules/${scheduleId}`);
            await loadSchedules(selectedEmployee.id);
        } catch (e) {
            console.error("Error deleting schedule", e);
            alert("Error al eliminar el horario.");
        }
    }

    onMount(() => {
        loadEmployees();
    });

    $: filteredEmployees = employees.filter(e => 
        e.nombre.toLowerCase().includes(searchTerm.toLowerCase()) || 
        e.email.toLowerCase().includes(searchTerm.toLowerCase())
    );
</script>

<div class="flex h-[calc(100vh-100px)] gap-6">
    <!-- Left Panel: Employee List -->
    <div class="w-1/3 flex flex-col rounded-xl border border-gray-200 bg-white shadow-sm overflow-hidden">
        <div class="p-4 border-b border-gray-100 bg-gray-50">
            <h2 class="text-lg font-semibold text-gray-800 mb-3">Empleados</h2>
            <div class="relative">
                <Search class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={18} />
                <input 
                    bind:value={searchTerm}
                    type="text" 
                    placeholder="Buscar..." 
                    class="w-full rounded-lg border border-gray-200 py-2 pl-10 pr-4 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
            </div>
        </div>
        
        <div class="flex-1 overflow-y-auto p-2 space-y-1">
            {#if loadingEmployees}
                <div class="p-4 text-center text-gray-500">Cargando empleados...</div>
            {:else if filteredEmployees.length === 0}
                <div class="p-4 text-center text-gray-500">No se encontraron empleados.</div>
            {:else}
                {#each filteredEmployees as emp}
                    <button 
                        class="w-full flex items-center gap-3 p-3 rounded-lg transition-colors text-left
                        {selectedEmployee?.id === emp.id ? 'bg-blue-50 border-blue-200 ring-1 ring-blue-200' : 'hover:bg-gray-50'}"
                        on:click={() => selectEmployee(emp)}
                    >
                        <div class="h-10 w-10 rounded-full bg-gray-200 flex items-center justify-center text-gray-500">
                            <User size={20} />
                        </div>
                        <div class="overflow-hidden">
                            <p class="font-medium text-gray-900 truncate">{emp.nombre}</p>
                            <p class="text-xs text-gray-500 truncate">{emp.email}</p>
                        </div>
                    </button>
                {/each}
            {/if}
        </div>
    </div>

    <!-- Right Panel: Schedule Management -->
    <div class="flex-1 flex flex-col rounded-xl border border-gray-200 bg-white shadow-sm overflow-hidden">
        {#if selectedEmployee}
            <div class="p-6 border-b border-gray-100 flex justify-between items-center bg-gray-50">
                <div>
                    <h2 class="text-xl font-bold text-gray-800">Gestionar Horarios</h2>
                    <p class="text-gray-500 text-sm">Para: <span class="font-medium text-gray-900">{selectedEmployee.nombre}</span></p>
                </div>
                <div class="text-sm text-gray-400">ID: {selectedEmployee.id}</div>
            </div>

            <div class="p-6 flex-1 overflow-y-auto">
                <!-- Add Schedule Form -->
                <div class="mb-8 bg-blue-50/50 p-4 rounded-xl border border-blue-100">
                    <h3 class="text-sm font-semibold text-blue-900 mb-3 flex items-center gap-2">
                        <Plus size={16} /> Asignar Nuevo Horario
                    </h3>
                    <div class="flex flex-wrap gap-4 items-end">
                        <div class="flex-1 min-w-[150px]">
                            <label class="block text-xs font-medium text-gray-600 mb-1">Día</label>
                            <select bind:value={newSchedule.day_of_week} class="w-full rounded-lg border-gray-200 text-sm py-2 px-3 focus:ring-blue-500 focus:border-blue-500">
                                {#each daysOfWeek as day}
                                    <option value={day}>{day}</option>
                                {/each}
                            </select>
                        </div>
                        <div class="flex-1 min-w-[120px]">
                            <label class="block text-xs font-medium text-gray-600 mb-1">Entrada</label>
                            <input type="time" bind:value={newSchedule.start_time} class="w-full rounded-lg border-gray-200 text-sm py-2 px-3 focus:ring-blue-500 focus:border-blue-500" />
                        </div>
                        <div class="flex-1 min-w-[120px]">
                            <label class="block text-xs font-medium text-gray-600 mb-1">Salida</label>
                            <input type="time" bind:value={newSchedule.end_time} class="w-full rounded-lg border-gray-200 text-sm py-2 px-3 focus:ring-blue-500 focus:border-blue-500" />
                        </div>
                        <button 
                            on:click={addSchedule}
                            class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors flex items-center gap-2"
                        >
                            Asignar
                        </button>
                    </div>
                </div>

                <!-- Schedule List -->
                <h3 class="text-sm font-semibold text-gray-700 mb-4 flex items-center gap-2">
                    <Calendar size={16} /> Horarios Asignados
                </h3>

                {#if loadingSchedules}
                    <div class="text-center py-8 text-gray-500">Cargando horarios...</div>
                {:else if schedules.length === 0}
                    <div class="text-center py-8 bg-gray-50 rounded-lg border border-dashed border-gray-200">
                        <p class="text-gray-500 text-sm">No hay horarios asignados para este empleado.</p>
                    </div>
                {:else}
                    <div class="grid gap-3">
                        {#each schedules as schedule}
                            <div class="flex items-center justify-between p-4 rounded-lg border border-gray-100 bg-white hover:shadow-sm transition-shadow">
                                <div class="flex items-center gap-4">
                                    <div class="h-10 w-10 rounded-lg bg-indigo-50 flex items-center justify-center text-indigo-600 font-bold text-xs uppercase">
                                        {schedule.day_of_week.substring(0, 3)}
                                    </div>
                                    <div>
                                        <p class="font-medium text-gray-900">{schedule.day_of_week}</p>
                                        <p class="text-sm text-gray-500 flex items-center gap-1">
                                            <Clock size={14} /> {schedule.start_time} - {schedule.end_time}
                                        </p>
                                    </div>
                                </div>
                                <button 
                                    on:click={() => deleteSchedule(schedule.id)}
                                    class="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                                    title="Eliminar horario"
                                >
                                    <Trash2 size={18} />
                                </button>
                            </div>
                        {/each}
                    </div>
                {/if}
            </div>
        {:else}
            <div class="flex-1 flex flex-col items-center justify-center text-gray-400 p-8">
                <div class="h-16 w-16 bg-gray-100 rounded-full flex items-center justify-center mb-4">
                    <User size={32} />
                </div>
                <p class="text-lg font-medium text-gray-500">Selecciona un empleado</p>
                <p class="text-sm">Elige un empleado de la lista para gestionar sus horarios.</p>
            </div>
        {/if}
    </div>
</div>
