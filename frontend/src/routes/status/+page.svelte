<script>
    import { onMount } from "svelte";
    import api from "$lib/utils/api";
    // Agregamos iconos necesarios
    import {
        Trash2,
        Plus,
        Loader2,
        Save,
        X,
        Pencil,
        AlertTriangle,
    } from "lucide-svelte";

    let statuses = [];
    let loading = true;
    let error = "";

    // Modal de Creación/Edición
    let showModal = false;
    let creating = false;
    let isEditing = false; // Nuevo: Controla si es edición o creación

    // Modal de Eliminación
    let showDeleteModal = false;
    let statusToDelete = null;

    // Form data for new/edit status
    let currentStatus = {
        id: null, // Necesario para edición
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

    async function saveStatus() {
        creating = true;
        error = "";
        try {
            if (isEditing) {
                await api.put(
                    `/nomina/statuses/${currentStatus.id}`,
                    currentStatus,
                );
            } else {
                await api.post("/nomina/statuses", currentStatus);
            }

            await loadStatuses();
            closeModal();
        } catch (e) {
            console.error(e);
            error = e.response?.data?.detail || "Error al guardar el status.";
        } finally {
            creating = false;
        }
    }

    function openCreateModal() {
        isEditing = false;
        currentStatus = {
            id: null,
            name: "",
            base_hourly_rate: 0,
            overtime_rate: 0,
            monthly_bonus: 0,
        };
        showModal = true;
    }

    function openEditModal(status) {
        isEditing = true;
        currentStatus = { ...status }; // Copia para no mutar directo
        showModal = true;
    }

    function closeModal() {
        showModal = false;
        isEditing = false;
        error = "";
    }

    // --- Lógica del Modal de Eliminación ---

    function openDeleteModal(id) {
        statusToDelete = id;
        showDeleteModal = true;
    }

    function closeDeleteModal() {
        showDeleteModal = false;
        statusToDelete = null;
    }

    async function confirmDelete() {
        if (!statusToDelete) return;

        try {
            await api.delete(`/nomina/statuses/${statusToDelete}`);
            await loadStatuses();
        } catch (e) {
            console.error(e);
            // Si falla, mostramos el error general (podríamos usar otro modal/toast)
            alert(
                e.response?.data?.detail ||
                    "Error al eliminar. Puede que esté en uso.",
            );
        } finally {
            closeDeleteModal();
        }
    }
</script>

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
                            Eliminar Status
                        </h3>
                        <div class="mt-2">
                            <p class="text-sm text-gray-500 dark:text-gray-400">
                                ¿Estás seguro de que deseas eliminar este
                                registro? Esta acción no se puede deshacer.
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
    <div>
        <h1 class="text-2xl font-bold text-gray-800 dark:text-white">
            Gestión de Cargos / Status
        </h1>
        <p class="text-sm text-gray-500 dark:text-gray-400">
            Administre los tipos de contratación y sus reglas salariales.
        </p>
    </div>
    <button
        on:click={openCreateModal}
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
                            <div class="flex items-center justify-end gap-2">
                                <button
                                    on:click={() => openEditModal(status)}
                                    class="rounded-lg p-2 text-blue-600 hover:bg-blue-50 dark:text-blue-400 dark:hover:bg-blue-900/20"
                                >
                                    <Pencil size={18} />
                                </button>
                                <button
                                    on:click={() => openDeleteModal(status.id)}
                                    class="rounded-lg p-2 text-red-600 hover:bg-red-50 dark:text-red-400 dark:hover:bg-red-900/20"
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
                    {isEditing ? "Editar Status" : "Nuevo Status"}
                </h3>
                <button
                    on:click={closeModal}
                    class="text-gray-500 hover:text-gray-700"
                >
                    <X size={20} />
                </button>
            </div>

            <form on:submit|preventDefault={saveStatus} class="space-y-4">
                <div>
                    <label
                        class="mb-1 block text-sm font-medium text-gray-700 dark:text-gray-300"
                        >Nombre</label
                    >
                    <input
                        type="text"
                        bind:value={currentStatus.name}
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
                            bind:value={currentStatus.base_hourly_rate}
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
                            bind:value={currentStatus.overtime_rate}
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
                        bind:value={currentStatus.monthly_bonus}
                        class="block w-full rounded-lg border border-gray-300 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                    />
                </div>

                <div class="mt-6 flex justify-end gap-3">
                    <button
                        type="button"
                        on:click={closeModal}
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
