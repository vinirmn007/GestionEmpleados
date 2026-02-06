<script>
    import { onMount } from "svelte";
    import api from "$lib/utils/api";

    let payrolls = [];
    let loading = false;

    async function generatePayroll() {
        loading = true;
        try {
            await api.post("/nomina/payrolls/generate", {
                month: 12,
                year: 2024,
                user_id: "ALL",
            });
            alert("Proceso de nómina iniciado");
            loadPayrolls();
        } catch (e) {
            alert("Error generando nómina: " + e.message);
        } finally {
            loading = false;
        }
    }

    async function loadPayrolls() {
        payrolls = [
            {
                employee: "Ana Martinez",
                gross: 2500,
                net: 2150,
                status: "Pendiente",
            },
            {
                employee: "Carlos Rodriguez",
                gross: 3200,
                net: 2720,
                status: "Pagado",
            },
        ];
    }

    onMount(loadPayrolls);
</script>

<div class="space-y-6">
    <div class="flex items-center justify-between">
        <h1 class="text-2xl font-bold text-gray-800 dark:text-white">
            Detalle de Roles de Pago
        </h1>
        <button
            on:click={generatePayroll}
            class="rounded-lg bg-blue-600 px-4 py-2 text-white shadow hover:bg-blue-700"
        >
            Enviar al Gestor de Pagos
        </button>
    </div>

    <div
        class="flex gap-4 rounded-lg bg-white dark:bg-gray-800 p-4 shadow-sm border border-gray-200 dark:border-gray-700"
    >
        <select
            class="rounded border border-gray-200 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 px-3 py-2 text-gray-700 dark:text-gray-300"
        >
            <option>Período: Junio 2024</option>
        </select>
        <select
            class="rounded border border-gray-200 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 px-3 py-2 text-gray-700 dark:text-gray-300"
        >
            <option>Estado: Pendiente</option>
        </select>
    </div>

    <div
        class="rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 shadow-sm"
    >
        <table class="w-full text-left">
            <thead
                class="bg-gray-50 dark:bg-gray-800/50 text-sm font-semibold text-gray-600 dark:text-gray-400 border-b border-gray-200 dark:border-gray-700"
            >
                <tr>
                    <th class="p-4">Empleado</th>
                    <th class="p-4">Sueldo Bruto</th>
                    <th class="p-4">Sueldo Neto</th>
                    <th class="p-4">Estado</th>
                </tr>
            </thead>
            <tbody class="divide-y divide-gray-100 dark:divide-gray-700">
                {#each payrolls as row}
                    <tr
                        class="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors"
                    >
                        <td class="p-4 text-gray-900 dark:text-white"
                            >{row.employee}</td
                        >
                        <td class="p-4 text-gray-600 dark:text-gray-400"
                            >${row.gross.toFixed(2)}</td
                        >
                        <td class="p-4 font-bold text-gray-900 dark:text-white"
                            >${row.net.toFixed(2)}</td
                        >
                        <td class="p-4">
                            <span
                                class={`rounded px-2 py-1 text-xs font-bold ${
                                    row.status === "Pagado"
                                        ? "bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400"
                                        : "bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-400"
                                }`}
                            >
                                {row.status}
                            </span>
                        </td>
                    </tr>
                {/each}
            </tbody>
        </table>
    </div>
</div>
