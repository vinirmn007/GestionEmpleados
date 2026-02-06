<script>
    import api from "$lib/utils/api";
    import { onMount } from "svelte";

    let config = {
        normalHour: 25.0,
        overtimeHour: 37.5,
        nightHour: 30.0,
        lateness: 0.5,
        absence: 200.0,
    };

    async function saveConfig() {
        try {
            alert("Configuración guardada correctamente");
        } catch (e) {
            alert("Error guardando configuración");
        }
    }
</script>

<div class="max-w-4xl mx-auto space-y-6">
    <h1 class="text-2xl font-bold text-gray-800 dark:text-white">
        Configuración de Nómina
    </h1>
    <p class="text-gray-500 dark:text-gray-400">
        Estos valores se aplicarán a todos los cálculos futuros.
    </p>

    <div
        class="grid gap-6 rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 p-8 shadow-sm"
    >
        <h2 class="text-lg font-semibold text-gray-800 dark:text-white">
            Valores por Hora
        </h2>

        <div class="grid grid-cols-2 gap-6">
            <div>
                <label
                    class="mb-1 block text-sm font-medium text-gray-700 dark:text-gray-300"
                    >Pago por Hora Normal</label
                >
                <div class="relative">
                    <span
                        class="absolute left-3 top-2 text-gray-500 dark:text-gray-400"
                        >$</span
                    >
                    <input
                        bind:value={config.normalHour}
                        type="number"
                        class="w-full rounded border border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-700 px-8 py-2 text-gray-900 dark:text-white"
                    />
                </div>
            </div>
            <div>
                <label
                    class="mb-1 block text-sm font-medium text-gray-700 dark:text-gray-300"
                    >Valor Hora Extra</label
                >
                <div class="relative">
                    <span
                        class="absolute left-3 top-2 text-gray-500 dark:text-gray-400"
                        >$</span
                    >
                    <input
                        bind:value={config.overtimeHour}
                        type="number"
                        class="w-full rounded border border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-700 px-8 py-2 text-gray-900 dark:text-white"
                    />
                </div>
            </div>
        </div>

        <div class="border-t border-gray-200 dark:border-gray-700 pt-6">
            <h2
                class="text-lg font-semibold text-gray-800 dark:text-white mb-4"
            >
                Otros Valores (Deducciones)
            </h2>
            <div class="grid grid-cols-2 gap-6">
                <div>
                    <label
                        class="mb-1 block text-sm font-medium text-gray-700 dark:text-gray-300"
                        >Valor por Atraso (minuto)</label
                    >
                    <div class="relative">
                        <span
                            class="absolute left-3 top-2 text-gray-500 dark:text-gray-400"
                            >$</span
                        >
                        <input
                            bind:value={config.lateness}
                            type="number"
                            class="w-full rounded border border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-700 px-8 py-2 text-gray-900 dark:text-white"
                        />
                    </div>
                </div>
                <div>
                    <label
                        class="mb-1 block text-sm font-medium text-gray-700 dark:text-gray-300"
                        >Deducción por Ausencia (día)</label
                    >
                    <div class="relative">
                        <span
                            class="absolute left-3 top-2 text-gray-500 dark:text-gray-400"
                            >$</span
                        >
                        <input
                            bind:value={config.absence}
                            type="number"
                            class="w-full rounded border border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-700 px-8 py-2 text-gray-900 dark:text-white"
                        />
                    </div>
                </div>
            </div>
        </div>

        <div
            class="flex justify-end gap-4 border-t border-gray-200 dark:border-gray-700 pt-6"
        >
            <button
                class="rounded-lg bg-gray-100 dark:bg-gray-700 px-6 py-2 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600"
                >Cancelar</button
            >
            <button
                on:click={saveConfig}
                class="rounded-lg bg-blue-600 px-6 py-2 text-white hover:bg-blue-700"
                >Guardar Cambios</button
            >
        </div>
    </div>
</div>
