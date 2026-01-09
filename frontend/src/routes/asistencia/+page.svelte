<script>
    import { onMount } from 'svelte';
    import api from '$lib/utils/api'; // Tu cliente Axios
    import { Calendar, RefreshCw, Search, Clock, User, ArrowDown, ArrowUp } from 'lucide-svelte';

    // Estado
    let loading = false;
    let reporte = [];
    let selectedDate = new Date().toISOString().split('T')[0]; // Hoy por defecto (YYYY-MM-DD)
    let searchTerm = '';

    // Cargar datos al montar
    onMount(() => {
        fetchReporte();
    });

    async function fetchReporte() {
        loading = true;
        reporte = [];
        try {
            // Llamamos a tu nuevo endpoint optimizado
            const { data } = await api.get('/attendance/reporte', {
                params: { target_date: selectedDate }
            });
            reporte = data;
        } catch (error) {
            console.error("Error al cargar reporte:", error);
            // Aquí podrías poner una alerta de error
        } finally {
            loading = false;
        }
    }

    // -- Helpers para visualización --

    // Formatear hora (ej: 08:30 AM)
    const formatTime = (isoString) => {
        if (!isoString) return '';
        return new Date(isoString).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    };

    // Calcular duración total basado en las marcas crudas
    // (Idealmente esto se mueve al backend luego, pero el front lo hace por ahora)
    function calculateDuration(marks) {
        if (!marks || marks.length < 2) return "0h 0m";

        let totalMs = 0;
        // Asumimos pares: [Entrada, Salida, Entrada, Salida...]
        // Ordenamos por si acaso
        const sorted = [...marks].sort((a, b) => new Date(a) - new Date(b));

        for (let i = 0; i < sorted.length - 1; i += 2) {
            const inTime = new Date(sorted[i]);
            const outTime = new Date(sorted[i+1]);
            totalMs += (outTime - inTime);
        }
        
        const hours = Math.floor(totalMs / (1000 * 60 * 60));
        const minutes = Math.floor((totalMs % (1000 * 60 * 60)) / (1000 * 60));
        
        return `${hours}h ${minutes}m`;
    }

    // Filtrado reactivo (Buscador)
    $: filteredReport = reporte.filter(item => 
        item.nombre.toLowerCase().includes(searchTerm.toLowerCase())
    );
</script>

<div class="p-6">
    <div class="mb-8 flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
            <h1 class="text-2xl font-bold text-gray-800">Reporte Diario de Asistencia</h1>
            <p class="text-sm text-gray-500">Vista consolidada de usuarios y marcaciones.</p>
        </div>

        <div class="flex items-center gap-3 bg-white p-2 rounded-lg shadow-sm border border-gray-100">
            <div class="relative">
                <Calendar class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={18} />
                <input 
                    type="date" 
                    bind:value={selectedDate} 
                    on:change={fetchReporte}
                    class="rounded-md border-0 bg-transparent py-1.5 pl-10 pr-2 text-gray-700 focus:ring-2 focus:ring-blue-500 outline-none text-sm font-medium"
                />
            </div>
            <div class="h-6 w-px bg-gray-200"></div>
            <button 
                on:click={fetchReporte} 
                class="p-2 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded-full transition-all"
                title="Actualizar datos"
            >
                <RefreshCw size={18} class={loading ? 'animate-spin' : ''} />
            </button>
        </div>
    </div>

    <div class="mb-6 max-w-md">
        <div class="relative">
            <Search class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
            <input 
                bind:value={searchTerm}
                type="text" 
                placeholder="Buscar empleado..." 
                class="w-full rounded-xl border border-gray-200 bg-white py-2.5 pl-10 pr-4 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200 transition-all"
            />
        </div>
    </div>

    <div class="overflow-hidden rounded-xl border border-gray-200 bg-white shadow-sm">
        <div class="overflow-x-auto">
            <table class="w-full text-left border-collapse">
                <thead>
                    <tr class="bg-gray-50/50 border-b border-gray-200 text-xs uppercase tracking-wider text-gray-500 font-semibold">
                        <th class="px-6 py-4">Empleado</th>
                        <th class="px-6 py-4">Historial de Marcas</th>
                        <th class="px-6 py-4 text-center">Estado Actual</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-gray-100">
                    {#if loading && reporte.length === 0}
                        {#each Array(3) as _}
                            <tr>
                                <td colspan="4" class="px-6 py-4"><div class="h-8 bg-gray-100 rounded animate-pulse w-full"></div></td>
                            </tr>
                        {/each}
                    {:else if filteredReport.length === 0}
                        <tr>
                            <td colspan="4" class="px-6 py-12 text-center text-gray-400">
                                <div class="flex flex-col items-center gap-2">
                                    <User size={32} class="opacity-20"/>
                                    <span>No hay registros para mostrar.</span>
                                </div>
                            </td>
                        </tr>
                    {:else}
                        {#each filteredReport as row}
                            <tr class="hover:bg-gray-50/80 transition-colors group">
                                <td class="px-6 py-4">
                                    <div class="flex items-center gap-3">
                                        <div class="h-10 w-10 rounded-full bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center text-white shadow-sm font-bold text-sm">
                                            {row.nombre.charAt(0).toUpperCase()}
                                        </div>
                                        <div>
                                            <div class="font-medium text-gray-900">{row.nombre}</div>
                                            <div class="text-xs text-gray-400 font-mono">ID: {row.user_id}</div>
                                        </div>
                                    </div>
                                </td>

                                <td class="px-6 py-4">
                                    <div class="flex flex-wrap gap-2 max-w-md">
                                        {#if row.marcas && row.marcas.length > 0}
                                            {#each row.marcas as marca, i}
                                                <div class="flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-medium border
                                                    {i % 2 === 0 
                                                        ? 'bg-emerald-50 text-emerald-700 border-emerald-100' 
                                                        : 'bg-amber-50 text-amber-700 border-amber-100'}"
                                                >
                                                    {#if i % 2 === 0}
                                                        <ArrowDown size={12} strokeWidth={3}/> {:else}
                                                        <ArrowUp size={12} strokeWidth={3}/>   {/if}
                                                    {formatTime(marca)}
                                                </div>
                                            {/each}
                                        {:else}
                                            <span class="text-xs text-gray-400 italic px-2">Sin actividad</span>
                                        {/if}
                                    </div>
                                </td>

                                <td class="px-6 py-4 text-center">
                                    {#if row.estado === 'Adentro'}
                                        <span class="inline-flex items-center gap-1.5 rounded-full bg-green-100 px-3 py-1 text-xs font-bold text-green-700 ring-1 ring-inset ring-green-600/20">
                                            <span class="relative flex h-2 w-2">
                                              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                                              <span class="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
                                            </span>
                                            EN TURNO
                                        </span>
                                    {:else}
                                        <span class="inline-flex items-center rounded-full bg-gray-100 px-3 py-1 text-xs font-bold text-gray-600 ring-1 ring-inset ring-gray-500/10">
                                            SALIDA
                                        </span>
                                    {/if}
                                </td>
                            </tr>
                        {/each}
                    {/if}
                </tbody>
            </table>
        </div>
    </div>
</div>