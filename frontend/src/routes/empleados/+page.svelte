<script>
    import { onMount } from 'svelte';
    import api from '$lib/utils/api';
    import { Search, Plus, Filter } from 'lucide-svelte';

    let empleados = [];
    let search = '';
    
    // Filtros
    let department = 'Todos';
    let status = 'Todos';

    async function loadEmpleados() {
        try {
            // Nota: User Service necesita un endpoint GET /usuarios
            const { data } = await api.get('/usuarios/usuarios'); 
            empleados = data;
        } catch (e) {
            console.error("Error cargando empleados", e);
            // Fallback data para visualización si el back falla
            empleados = [
                { id: 'EMP-001', name: 'Ana García Pérez', dept: 'Tecnología', job: 'Dev Senior', status: 'Activo' },
                { id: 'EMP-002', name: 'Carlos Ruiz', dept: 'Ventas', job: 'Gerente', status: 'Activo' },
            ];
        }
    }

    onMount(loadEmpleados);
</script>

<div class="mb-6 flex items-center justify-between">
    <h1 class="text-2xl font-bold text-gray-800">Dashboard de Empleados</h1>
    <a href="/empleados/nuevo" class="flex items-center gap-2 rounded-lg bg-blue-600 px-4 py-2 text-white hover:bg-blue-700">
        <Plus size={20} /> Añadir Nuevo Empleado
    </a>
</div>

<div class="rounded-xl border border-gray-200 bg-white p-4 shadow-sm">
    <div class="mb-6 flex flex-wrap gap-4">
        <div class="relative flex-1">
            <Search class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
            <input 
                bind:value={search}
                type="text" 
                placeholder="Buscar empleados por nombre o ID" 
                class="w-full rounded-lg border border-gray-200 py-2 pl-10 pr-4 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
        </div>
        <select class="rounded-lg border bg-white px-4 py-2 text-gray-600">
            <option>Departamento</option>
        </select>
        <select class="rounded-lg border bg-white px-4 py-2 text-gray-600">
            <option>Estado</option>
        </select>
    </div>

    <div class="overflow-x-auto">
        <table class="w-full text-left">
            <thead class="border-b bg-gray-50 text-sm font-semibold text-gray-600">
                <tr>
                    <th class="px-6 py-4">Nombre Completo</th>
                    <th class="px-6 py-4">ID Empleado</th>
                    <th class="px-6 py-4">Departamento</th>
                    <th class="px-6 py-4">Puesto</th>
                    <th class="px-6 py-4">Estado</th>
                    <th class="px-6 py-4">Acciones</th>
                </tr>
            </thead>
            <tbody class="divide-y">
                {#each empleados as emp}
                    <tr class="hover:bg-gray-50">
                        <td class="flex items-center gap-3 px-6 py-4">
                            <div class="h-10 w-10 rounded-full bg-gray-200"></div> <span class="font-medium text-gray-900">{emp.name}</span>
                        </td>
                        <td class="px-6 py-4 text-gray-500">{emp.id}</td>
                        <td class="px-6 py-4 text-gray-500">{emp.dept}</td>
                        <td class="px-6 py-4 text-gray-500">{emp.job}</td>
                        <td class="px-6 py-4">
                            <span class="rounded-full bg-green-100 px-3 py-1 text-xs font-semibold text-green-700">
                                {emp.status}
                            </span>
                        </td>
                        <td class="px-6 py-4 text-gray-400">...</td>
                    </tr>
                {/each}
            </tbody>
        </table>
    </div>
</div>