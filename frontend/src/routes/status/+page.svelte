<script>
    import { onMount } from "svelte";
    import api from "$lib/utils/api";
    import { Trash2, Plus, Loader2, Save, X } from "lucide-svelte";

    let statuses = [];
    let loading = true;
    let error = "";
    let showModal = false;
    let creating = false;

    // Form data for new status
    let newStatus = {
        name: "",
        base_hourly_rate: 0,
        overtime_rate: 0,
        monthly_bonus: 0,
    };

    onMount(loadStatuses);

    async function loadStatuses() {
        loading = true;
        try {
            const { data } = await api.get("/nomina/statuses");
            statuses = data;
        } catch (e) {
            console.error(e);
            error = "No se pudieron cargar los status.";
        } finally {
            loading = false;
        }
    }

    async function createStatus() {
        creating = true;
        error = "";
        try {
            await api.post("/nomina/statuses", newStatus);
            await loadStatuses();
            showModal = false;
            newStatus = {
                name: "",
                base_hourly_rate: 0,
                overtime_rate: 0,
                monthly_bonus: 0,
            };
        } catch (e) {
            console.error(e);
            error = e.response?.data?.detail || "Error al crear el status.";
        } finally {
            creating = false;
        }
    }

    async function deleteStatus(id) {
        if (!confirm("¿Seguro que desea eliminar este status?")) return;
        try {
            await api.delete(`/nomina/statuses/${id}`);
            await loadStatuses();
        } catch (e) {
            console.error(e);
            alert("Error al eliminar. Puede que esté en uso.");
        }
    }
</script>

<div class="mb-6 flex items-center justify-between">
    <div>
        <h1 class="text-2xl font-bold text-gray-800 dark:text-white">
            Gestión de Cargos / Status
        </h1>
        <p class="text-sm text-gray-500 dark:text-gray-400">
            Administre los tipos de contratación y sus reglas salariales.
        </p>
    </div>
    <button
        on:click={() => (showModal = true)}
        class="flex items-center gap-2 rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
    >
        <Plus size={18} /> Nuevo Status
    </button>
</div>

{#if error}
    <div class="mb-4 rounded-lg bg-red-50 p-4 text-red-800">{error}</div>
{/if}

{#if loading}
    <div class="flex justify-center p-8">
        <Loader2 class="animate-spin text-gray-400" size={32} />
    </div>
{:else}
    <div
        class="overflow-hidden rounded-xl border border-gray-200 bg-white shadow-sm dark:border-gray-700 dark:bg-gray-800"
    >
        <table
            class="w-full text-left text-sm text-gray-500 dark:text-gray-400"
        >
            <thead
                class="bg-gray-50 text-xs uppercase text-gray-700 dark:bg-gray-700 dark:text-gray-400"
            >
                <tr>
                    <th class="px-6 py-3">Nombre</th>
                    <th class="px-6 py-3">Pago Hora</th>
                    <th class="px-6 py-3">Hora Extra</th>
                    <th class="px-6 py-3">Bono Mensual</th>
                    <th class="px-6 py-3 text-right">Acciones</th>
                </tr>
            </thead>
            <tbody>
                {#each statuses as status}
                    <tr
                        class="border-b bg-white hover:bg-gray-50 dark:border-gray-700 dark:bg-gray-800 dark:hover:bg-gray-700"
                    >
                        <td
                            class="px-6 py-4 font-medium text-gray-900 dark:text-white"
                            >{status.name}</td
                        >
                        <td class="px-6 py-4">${status.base_hourly_rate}</td>
                        <td class="px-6 py-4">${status.overtime_rate}</td>
                        <td class="px-6 py-4">${status.monthly_bonus}</td>
                        <td class="px-6 py-4 text-right">
                            <button
                                on:click={() => deleteStatus(status.id)}
                                class="rounded-lg p-2 text-red-600 hover:bg-red-50 dark:text-red-400 dark:hover:bg-red-900/20"
                            >
                                <Trash2 size={18} />
                            </button>
                        </td>
                    </tr>
                {/each}
            </tbody>
        </table>
    </div>
{/if}

{#if showModal}
    <div
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4"
    >
        <div
            class="w-full max-w-md rounded-xl bg-white p-6 shadow-xl dark:bg-gray-800"
        >
            <div class="mb-4 flex items-center justify-between">
                <h3 class="text-lg font-bold text-gray-900 dark:text-white">
                    Nuevo Status
                </h3>
                <button
                    on:click={() => (showModal = false)}
                    class="text-gray-500 hover:text-gray-700"
                >
                    <X size={20} />
                </button>
            </div>

            <form on:submit|preventDefault={createStatus} class="space-y-4">
                <div>
                    <label
                        class="mb-1 block text-sm font-medium text-gray-700 dark:text-gray-300"
                        >Nombre</label
                    >
                    <input
                        type="text"
                        bind:value={newStatus.name}
                        required
                        class="block w-full rounded-lg border border-gray-300 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                        placeholder="Ej. Tiempo Completo"
                    />
                </div>
                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label
                            class="mb-1 block text-sm font-medium text-gray-700 dark:text-gray-300"
                            >Pago Hora</label
                        >
                        <input
                            type="number"
                            step="0.01"
                            bind:value={newStatus.base_hourly_rate}
                            required
                            class="block w-full rounded-lg border border-gray-300 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                        />
                    </div>
                    <div>
                        <label
                            class="mb-1 block text-sm font-medium text-gray-700 dark:text-gray-300"
                            >Hora Extra</label
                        >
                        <input
                            type="number"
                            step="0.01"
                            bind:value={newStatus.overtime_rate}
                            required
                            class="block w-full rounded-lg border border-gray-300 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                        />
                    </div>
                </div>
                <div>
                    <label
                        class="mb-1 block text-sm font-medium text-gray-700 dark:text-gray-300"
                        >Bono Mensual</label
                    >
                    <input
                        type="number"
                        step="0.01"
                        bind:value={newStatus.monthly_bonus}
                        class="block w-full rounded-lg border border-gray-300 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                    />
                </div>

                <div class="mt-6 flex justify-end gap-3">
                    <button
                        type="button"
                        on:click={() => (showModal = false)}
                        class="rounded-lg border border-gray-300 px-4 py-2 text-sm font-medium hover:bg-gray-50 dark:border-gray-600 dark:text-white dark:hover:bg-gray-700"
                    >
                        Cancelar
                    </button>
                    <button
                        type="submit"
                        disabled={creating}
                        class="flex items-center gap-2 rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-50"
                    >
                        {#if creating}
                            <Loader2 class="animate-spin" size={16} />
                        {/if}
                        Guardar
                    </button>
                </div>
            </form>
        </div>
    </div>
{/if}
