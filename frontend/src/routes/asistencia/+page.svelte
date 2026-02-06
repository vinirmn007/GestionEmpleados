<script>
    import { onMount } from "svelte";
    import api from "$lib/utils/api";
    import {
        Calendar,
        RefreshCw,
        Search,
        Clock,
        User,
        ArrowDown,
        ArrowUp,
        Edit,
        Trash2,
        Plus,
        X,
        Save,
        Check,
        AlertTriangle,
    } from "lucide-svelte";

    let loading = false;
    let reporte = [];
    let selectedDate = new Date().toISOString().split("T")[0];
    let searchTerm = "";

    // Modal state
    let showModal = false;
    let editingUser = null;
    let editingMarks = [];

    let newMarkTime = "";

    // Delete Modal State
    let showDeleteModal = false;
    let markToDeleteIndex = null;

    onMount(() => {
        fetchReporte();
    });

    async function fetchReporte() {
        loading = true;
        reporte = [];
        try {
            const { data } = await api.get("/attendance/reporte", {
                params: { target_date: selectedDate },
            });
            reporte = data;
        } catch (error) {
            console.error("Error al cargar reporte:", error);
        } finally {
            loading = false;
        }
    }

    const formatTime = (isoString) => {
        if (!isoString) return "";
        return new Date(isoString).toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
        });
    };

    function calculateDuration(marks) {
        if (!marks || marks.length < 2) return "0h 0m";

        let totalMs = 0;
        // Extract timestamps from objects if needed
        const timestamps = marks.map((m) => (m.timestamp ? m.timestamp : m));
        const sorted = [...timestamps].sort(
            (a, b) => new Date(a) - new Date(b),
        );

        for (let i = 0; i < sorted.length - 1; i += 2) {
            const inTime = new Date(sorted[i]);
            const outTime = new Date(sorted[i + 1]);
            totalMs += outTime - inTime;
        }

        const hours = Math.floor(totalMs / (1000 * 60 * 60));
        const minutes = Math.floor((totalMs % (1000 * 60 * 60)) / (1000 * 60));

        return `${hours}h ${minutes}m`;
    }

    function openEditModal(user) {
        editingUser = user;
        // Deep copy marks to avoid mutating directly
        editingMarks = user.marcas.map((m) => ({ ...m }));
        showModal = true;
    }

    function closeEditModal() {
        showModal = false;
        editingUser = null;
        editingMarks = [];
        newMarkTime = "";
    }

    async function saveMarkChange(index) {
        const mark = editingMarks[index];
        try {
            await api.put(`/attendance/mark/${mark.id}`, {
                timestamp: mark.timestamp,
            });
            // Refresh
            await fetchReporte();
            // Update local state to reflect change (optional, but good for UX)
            // But fetchReporte will overwrite everything anyway
            alert("Marca actualizada");
        } catch (error) {
            console.error("Error updating mark:", error);
            alert("Error al actualizar marca");
        }
    }

    function openDeleteModal(index) {
        markToDeleteIndex = index;
        showDeleteModal = true;
    }

    function closeDeleteModal() {
        showDeleteModal = false;
        markToDeleteIndex = null;
    }

    async function confirmDelete() {
        if (markToDeleteIndex === null) return;
        const mark = editingMarks[markToDeleteIndex];
        try {
            await api.delete(`/attendance/mark/${mark.id}`);
            editingMarks.splice(markToDeleteIndex, 1);
            editingMarks = editingMarks; // trigger reactivity
            await fetchReporte();
        } catch (error) {
            console.error("Error deleting mark:", error);
            alert("Error al eliminar marca");
        } finally {
            closeDeleteModal();
        }
    }

    async function addManualMark() {
        if (!newMarkTime) return;

        // combine selectedDate and newMarkTime
        // newMarkTime is HH:mm
        // selectedDate is YYYY-MM-DD
        const dateTimeStr = `${selectedDate}T${newMarkTime}:00`;
        const dateObj = new Date(dateTimeStr);
        const isoStr = dateObj.toISOString();

        try {
            const payload = {
                user_id: String(editingUser.user_id),
                timestamp: isoStr,
            };
            console.log("Sending manual mark payload:", payload);
            const { data } = await api.post("/attendance/mark/manual", payload);
            editingMarks = [
                ...editingMarks,
                { id: data.id, timestamp: data.timestamp },
            ];
            newMarkTime = "";
            await fetchReporte();
        } catch (error) {
            console.error("Error adding mark:", error);
            alert(
                "Error al agregar marca: " +
                    (error.response?.data?.detail || error.message),
            );
        }
    }

    $: filteredReport = reporte.filter((item) =>
        item.nombre.toLowerCase().includes(searchTerm.toLowerCase()),
    );
</script>

<div class="p-6">
    <div
        class="mb-8 flex flex-col gap-4 md:flex-row md:items-center md:justify-between"
    >
        <div>
            <h1 class="text-2xl font-bold text-gray-800 dark:text-white">
                Reporte Diario de Asistencia
            </h1>
            <p class="text-sm text-gray-500 dark:text-gray-400">
                Vista consolidada de usuarios y marcaciones.
            </p>
        </div>

        <div
            class="flex items-center gap-3 bg-white dark:bg-gray-800 p-2 rounded-lg shadow-sm border border-gray-100 dark:border-gray-700"
        >
            <div class="relative">
                <Calendar
                    class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 dark:text-gray-500"
                    size={18}
                />
                <input
                    type="date"
                    bind:value={selectedDate}
                    on:change={fetchReporte}
                    class="rounded-md border-0 bg-transparent py-1.5 pl-10 pr-2 text-gray-700 dark:text-gray-200 focus:ring-2 focus:ring-blue-500 outline-none text-sm font-medium"
                />
            </div>
            <div class="h-6 w-px bg-gray-200 dark:bg-gray-600"></div>
            <button
                on:click={fetchReporte}
                class="p-2 text-gray-500 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/20 rounded-full transition-all"
                title="Actualizar datos"
            >
                <RefreshCw size={18} class={loading ? "animate-spin" : ""} />
            </button>
        </div>
    </div>

    <div class="mb-6 max-w-md">
        <div class="relative">
            <Search
                class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 dark:text-gray-500"
                size={20}
            />
            <input
                bind:value={searchTerm}
                type="text"
                placeholder="Buscar empleado..."
                class="w-full rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 py-2.5 pl-10 pr-4 text-gray-900 dark:text-white shadow-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200 dark:focus:ring-blue-800 transition-all"
            />
        </div>
    </div>

    <div
        class="overflow-hidden rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 shadow-sm"
    >
        <div class="overflow-x-auto">
            <table class="w-full text-left border-collapse">
                <thead>
                    <tr
                        class="bg-gray-50/50 dark:bg-gray-800/50 border-b border-gray-200 dark:border-gray-700 text-xs uppercase tracking-wider text-gray-500 dark:text-gray-400 font-semibold"
                    >
                        <th class="px-6 py-4">Empleado</th>
                        <th class="px-6 py-4">Historial de Marcas</th>
                        <th class="px-6 py-4 text-center">Estado Actual</th>
                        <th class="px-6 py-4 text-right">Acciones</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-gray-100 dark:divide-gray-700">
                    {#if loading && reporte.length === 0}
                        {#each Array(3) as _}
                            <tr>
                                <td colspan="4" class="px-6 py-4"
                                    ><div
                                        class="h-8 bg-gray-100 dark:bg-gray-700 rounded animate-pulse w-full"
                                    ></div></td
                                >
                            </tr>
                        {/each}
                    {:else if filteredReport.length === 0}
                        <tr>
                            <td
                                colspan="4"
                                class="px-6 py-12 text-center text-gray-400 dark:text-gray-500"
                            >
                                <div class="flex flex-col items-center gap-2">
                                    <User size={32} class="opacity-20" />
                                    <span>No hay registros para mostrar.</span>
                                </div>
                            </td>
                        </tr>
                    {:else}
                        {#each filteredReport as row}
                            <tr
                                class="hover:bg-gray-50/80 dark:hover:bg-gray-700/50 transition-colors group"
                            >
                                <td class="px-6 py-4">
                                    <div class="flex items-center gap-3">
                                        <div
                                            class="h-10 w-10 rounded-full bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center text-white shadow-sm font-bold text-sm"
                                        >
                                            {row.nombre.charAt(0).toUpperCase()}
                                        </div>
                                        <div>
                                            <div
                                                class="font-medium text-gray-900 dark:text-white"
                                            >
                                                {row.nombre}
                                            </div>
                                            <div
                                                class="text-xs text-gray-400 dark:text-gray-500 font-mono"
                                            >
                                                ID: {row.user_id}
                                            </div>
                                        </div>
                                    </div>
                                </td>

                                <td class="px-6 py-4">
                                    <div class="flex flex-wrap gap-2 max-w-md">
                                        {#if row.marcas && row.marcas.length > 0}
                                            {#each row.marcas as marca, i}
                                                <div
                                                    class="flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-medium border
                                                    {i % 2 === 0
                                                        ? 'bg-emerald-50 dark:bg-emerald-900/30 text-emerald-700 dark:text-emerald-300 border-emerald-100 dark:border-emerald-800'
                                                        : 'bg-amber-50 dark:bg-amber-900/30 text-amber-700 dark:text-amber-300 border-amber-100 dark:border-amber-800'}"
                                                >
                                                    {#if i % 2 === 0}
                                                        <ArrowDown
                                                            size={12}
                                                            strokeWidth={3}
                                                        />
                                                    {:else}
                                                        <ArrowUp
                                                            size={12}
                                                            strokeWidth={3}
                                                        />
                                                    {/if}
                                                    {formatTime(
                                                        marca.timestamp,
                                                    )}
                                                </div>
                                            {/each}
                                        {:else}
                                            <span
                                                class="text-xs text-gray-400 dark:text-gray-500 italic px-2"
                                                >Sin actividad</span
                                            >
                                        {/if}
                                    </div>
                                </td>

                                <td class="px-6 py-4 text-center">
                                    {#if row.estado === "Adentro"}
                                        <span
                                            class="inline-flex items-center gap-1.5 rounded-full bg-green-100 dark:bg-green-900/30 px-3 py-1 text-xs font-bold text-green-700 dark:text-green-400 ring-1 ring-inset ring-green-600/20 dark:ring-green-500/30"
                                        >
                                            <span class="relative flex h-2 w-2">
                                                <span
                                                    class="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"
                                                ></span>
                                                <span
                                                    class="relative inline-flex rounded-full h-2 w-2 bg-green-500"
                                                ></span>
                                            </span>
                                            EN TURNO
                                        </span>
                                    {:else}
                                        <span
                                            class="inline-flex items-center rounded-full bg-gray-100 dark:bg-gray-700 px-3 py-1 text-xs font-bold text-gray-600 dark:text-gray-300 ring-1 ring-inset ring-gray-500/10 dark:ring-gray-500/30"
                                        >
                                            SALIDA
                                        </span>
                                    {/if}
                                </td>
                                <td class="px-6 py-4 text-right">
                                    <button
                                        on:click={() => openEditModal(row)}
                                        class="p-2 text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
                                        title="Editar asistencia"
                                    >
                                        <Edit size={18} />
                                    </button>
                                </td>
                            </tr>
                        {/each}
                    {/if}
                </tbody>
            </table>
        </div>
    </div>
</div>

<!-- Edit Modal -->
{#if showModal}
    <div
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4"
    >
        <div
            class="w-full max-w-md rounded-2xl bg-white dark:bg-gray-800 p-6 shadow-xl"
        >
            <div class="mb-6 flex items-center justify-between">
                <h3 class="text-lg font-bold text-gray-900 dark:text-white">
                    Editar Asistencia
                </h3>
                <button
                    on:click={closeEditModal}
                    class="rounded-full p-1 text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                >
                    <X size={20} />
                </button>
            </div>

            <div class="mb-6">
                <div
                    class="flex items-center gap-3 mb-4 p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg"
                >
                    <div
                        class="h-10 w-10 rounded-full bg-blue-100 dark:bg-blue-800 flex items-center justify-center text-blue-600 dark:text-blue-200 font-bold"
                    >
                        {editingUser.nombre.charAt(0).toUpperCase()}
                    </div>
                    <div>
                        <div class="font-medium text-gray-900 dark:text-white">
                            {editingUser.nombre}
                        </div>
                        <div class="text-xs text-gray-500 mb-1">
                            {selectedDate}
                        </div>
                    </div>
                </div>

                <div class="space-y-3 max-h-[300px] overflow-y-auto pr-2">
                    {#each editingMarks as mark, i (mark.id)}
                        <div class="flex items-center gap-2">
                            <div class="relative flex-1">
                                <Clock
                                    class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"
                                    size={16}
                                />
                                <input
                                    type="time"
                                    value={new Date(
                                        mark.timestamp,
                                    ).toLocaleTimeString([], {
                                        hour: "2-digit",
                                        minute: "2-digit",
                                        hour12: false,
                                    })}
                                    on:change={(e) => {
                                        // Update local state temporarily
                                        const [h, m] =
                                            e.target.value.split(":");
                                        const d = new Date(mark.timestamp);
                                        d.setHours(h);
                                        d.setMinutes(m);
                                        editingMarks[i].timestamp =
                                            d.toISOString();
                                    }}
                                    class="w-full rounded-lg border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900 py-2 pl-9 pr-3 text-sm focus:border-blue-500 focus:outline-none"
                                />
                            </div>
                            <button
                                on:click={() => saveMarkChange(i)}
                                class="p-2 text-green-600 hover:bg-green-50 rounded-lg transition-colors"
                                title="Guardar cambios"
                            >
                                <Save size={18} />
                            </button>
                            <button
                                on:click={() => openDeleteModal(i)}
                                class="p-2 text-red-500 hover:bg-red-50 rounded-lg transition-colors"
                                title="Eliminar marca"
                            >
                                <Trash2 size={18} />
                            </button>
                        </div>
                    {/each}

                    {#if editingMarks.length === 0}
                        <div
                            class="text-center py-4 text-gray-500 text-sm italic"
                        >
                            No hay marcas registradas este día.
                        </div>
                    {/if}
                </div>

                <div
                    class="mt-4 pt-4 border-t border-gray-100 dark:border-gray-700"
                >
                    <label
                        class="block text-xs font-medium text-gray-500 mb-2 uppercase"
                        >Agregar nueva marca</label
                    >
                    <div class="flex gap-2">
                        <input
                            type="time"
                            bind:value={newMarkTime}
                            class="flex-1 rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none"
                        />
                        <button
                            on:click={addManualMark}
                            disabled={!newMarkTime}
                            class="flex items-center gap-2 rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                        >
                            <Plus size={16} />
                            Agregar
                        </button>
                    </div>
                </div>
            </div>

            <div class="flex justify-end">
                <button
                    on:click={closeEditModal}
                    class="rounded-lg px-4 py-2 text-sm font-medium text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                >
                    Cerrar
                </button>
            </div>
        </div>
    </div>
{/if}

<!-- Delete Confirmation Modal -->
{#if showDeleteModal}
    <div class="fixed inset-0 z-[60] flex items-center justify-center p-4">
        <div
            class="absolute inset-0 bg-gray-900/50 dark:bg-black/60 backdrop-blur-sm transition-opacity"
            on:click={closeDeleteModal}
        ></div>
        <div
            class="relative w-full max-w-sm rounded-xl bg-white dark:bg-gray-800 shadow-xl border border-gray-100 dark:border-gray-700 p-6"
        >
            <div class="flex flex-col items-center text-center gap-4">
                <div
                    class="h-12 w-12 rounded-full bg-red-50 dark:bg-red-900/20 flex items-center justify-center text-red-600 dark:text-red-400"
                >
                    <AlertTriangle size={24} />
                </div>
                <div>
                    <h3 class="text-lg font-bold text-gray-900 dark:text-white">
                        Confirmar eliminación
                    </h3>
                    <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">
                        ¿Estás seguro de que quieres eliminar esta marca? Esta
                        acción es irreversible.
                    </p>
                </div>
                <div class="flex gap-3 w-full mt-2">
                    <button
                        on:click={closeDeleteModal}
                        class="flex-1 rounded-lg border border-gray-200 dark:border-gray-600 py-2.5 text-sm font-medium text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-700"
                    >
                        Cancelar
                    </button>
                    <button
                        on:click={confirmDelete}
                        class="flex-1 rounded-lg bg-red-600 py-2.5 text-sm font-medium text-white hover:bg-red-700 shadow-sm"
                    >
                        Eliminar
                    </button>
                </div>
            </div>
        </div>
    </div>
{/if}
