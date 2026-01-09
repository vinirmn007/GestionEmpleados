<script>
    import { onMount } from 'svelte';
    import api from '$lib/utils/api';
    import { Search, Plus, Pencil, Trash2, MapPin } from 'lucide-svelte';

    let empleados = [];
    let search = '';
    
    // Filtros
    let department = 'Todos';
    let status = 'Todos';

    async function loadEmpleados() {
        try {
            const { data } = await api.get('/usuarios/list'); 
            empleados = data.data;
        } catch (e) {
            console.error("Error cargando empleados", e);
            // Fallback data con campo dirección añadido
            empleados = [
                { id: 'EMP-001', nombre: 'Ana García Pérez', correo: 'ana@example.com', dept: 'Tecnología', status: 'Activo', direccion: 'Av. Universitaria 123' },
                { id: 'EMP-002', nombre: 'Carlos Ruiz', correo: 'carlos@example.com', dept: 'Ventas', status: 'Activo', direccion: 'Calle Bolívar y Rocafuerte' },
                { id: 'EMP-003', nombre: 'Elena Torres', correo: 'elena@example.com', dept: 'RRHH', status: 'Inactivo', direccion: 'Barrio El Valle' },
            ];
        }
    }

    function handleEdit(id) {
        console.log("Editando usuario:", id);
        // Lógica de redirección o modal aquí
    }

    function handleDelete(id) {
        if(confirm("¿Estás seguro de eliminar este empleado?")) {
            async function deleteEmpleado() {
                try {
                    await api.delete(`/usuarios/delete/${id}`);
                    empleados = empleados.filter(emp => emp.id !== id);
                } catch (e) {
                    console.error("Error eliminando empleado", e);
                }
            }
        }
    }

    onMount(loadEmpleados);
</script>

<div class="mb-6 flex items-center justify-between">
    <h1 class="text-2xl font-bold text-gray-800">Dashboard de Empleados</h1>
    <a href="/empleados/nuevo" class="flex items-center gap-2 rounded-lg bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 shadow-sm transition-colors">
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
        <select class="rounded-lg border bg-white px-4 py-2 text-gray-600 focus:ring-2 focus:ring-blue-500 outline-none">
            <option>Departamento</option>
        </select>
        <select class="rounded-lg border bg-white px-4 py-2 text-gray-600 focus:ring-2 focus:ring-blue-500 outline-none">
            <option>Estado</option>
        </select>
    </div>

    <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse">
            <thead class="border-b bg-gray-50 text-sm font-semibold text-gray-600 uppercase tracking-wider">
                <tr>
                    <th class="px-6 py-4">Nombre Completo</th>
                    <th class="px-6 py-4">ID / Correo</th>
                    <th class="px-6 py-4">Dirección</th>
                    <th class="px-6 py-4">Estado</th>
                    <th class="px-6 py-4 text-center">Acciones</th>
                </tr>
            </thead>
            <tbody class="divide-y divide-gray-100">
                {#each empleados as emp}
                    <tr class="hover:bg-gray-50 transition-colors group">
                        <td class="px-6 py-4">
                            <div class="flex items-center gap-3">
                                <div class="h-10 w-10 rounded-full bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center text-white shadow-sm font-bold text-sm">
                                    {emp.nombre.charAt(0).toUpperCase()}
                                </div>
                                <span class="font-medium text-gray-900">{emp.nombre}</span>
                            </div>
                        </td>

                        <td class="px-6 py-4">
                            <div class="flex flex-col">
                                <span class="text-sm font-medium text-gray-700">{emp.id}</span>
                                <span class="text-xs text-gray-500">{emp.correo}</span>
                            </div>
                        </td>

                        <td class="px-6 py-4 text-gray-600 text-sm">
                            <div class="flex items-center gap-2">
                                <MapPin size={14} class="text-gray-400" />
                                <span class="truncate max-w-[200px]" title={emp.direccion}>
                                    {emp.direccion || 'Sin dirección registrada'}
                                </span>
                            </div>
                        </td>

                        <td class="px-6 py-4">
                            {#if emp.status === 'Activo'}
                                <span class="inline-flex items-center rounded-full bg-green-100 px-2.5 py-0.5 text-xs font-medium text-green-800">
                                    Activo
                                </span>
                            {:else}
                                <span class="inline-flex items-center rounded-full bg-gray-100 px-2.5 py-0.5 text-xs font-medium text-gray-800">
                                    Inactivo
                                </span>
                            {/if}
                        </td>

                        <td class="px-6 py-4">
                            <div class="flex items-center justify-center gap-2">
                                <button 
                                    on:click={() => handleEdit(emp.id)}
                                    class="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors" 
                                    title="Editar"
                                >
                                    <Pencil size={18} />
                                </button>
                                <button 
                                    on:click={() => handleDelete(emp.id)}
                                    class="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors" 
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