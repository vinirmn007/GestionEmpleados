<script>
    import { onMount } from 'svelte';
    import api from '$lib/utils/api';
    
    let payrolls = [];
    let loading = false;

    // Generar Rol Masivo
    async function generatePayroll() {
        loading = true;
        try {
            // Llama a Nomina Service a través de Kong
            // Endpoint: POST /payrolls/generate (Necesita payload del form, aquí simplificado)
            await api.post('/nomina/payrolls/generate', { 
                month: 12, 
                year: 2024, 
                user_id: "ALL" // Backend tendría que soportar "ALL" o hacer loop aquí
            });
            alert('Proceso de nómina iniciado');
            loadPayrolls();
        } catch (e) {
            alert('Error generando nómina: ' + e.message);
        } finally {
            loading = false;
        }
    }

    async function loadPayrolls() {
         // Endpoint hipotético para listar historial
         // const { data } = await api.get('/nomina/payrolls');
         // payrolls = data;
         payrolls = [
             { employee: 'Ana Martinez', gross: 2500, net: 2150, status: 'Pendiente' },
             { employee: 'Carlos Rodriguez', gross: 3200, net: 2720, status: 'Pagado' }
         ];
    }
    
    onMount(loadPayrolls);
</script>

<div class="space-y-6">
    <div class="flex items-center justify-between">
        <h1 class="text-2xl font-bold">Detalle de Roles de Pago</h1>
        <button on:click={generatePayroll} class="rounded-lg bg-blue-600 px-4 py-2 text-white shadow hover:bg-blue-700">
            Enviar al Gestor de Pagos
        </button>
    </div>

    <div class="flex gap-4 rounded-lg bg-white p-4 shadow-sm">
        <select class="rounded border bg-gray-50 px-3 py-2"><option>Período: Junio 2024</option></select>
        <select class="rounded border bg-gray-50 px-3 py-2"><option>Estado: Pendiente</option></select>
    </div>

    <div class="rounded-lg border bg-white shadow-sm">
        <table class="w-full text-left">
            <thead class="bg-gray-50 text-sm font-semibold text-gray-600">
                <tr>
                    <th class="p-4">Empleado</th>
                    <th class="p-4">Sueldo Bruto</th>
                    <th class="p-4">Sueldo Neto</th>
                    <th class="p-4">Estado</th>
                </tr>
            </thead>
            <tbody class="divide-y">
                {#each payrolls as row}
                    <tr>
                        <td class="p-4">{row.employee}</td>
                        <td class="p-4 text-gray-600">${row.gross.toFixed(2)}</td>
                        <td class="p-4 font-bold text-gray-900">${row.net.toFixed(2)}</td>
                        <td class="p-4">
                            <span class={`rounded px-2 py-1 text-xs font-bold ${
                                row.status === 'Pagado' ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'
                            }`}>
                                {row.status}
                            </span>
                        </td>
                    </tr>
                {/each}
            </tbody>
        </table>
    </div>
</div>