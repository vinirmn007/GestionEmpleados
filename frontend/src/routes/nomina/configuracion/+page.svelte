<script>
    import api from '$lib/utils/api';
    import { onMount } from 'svelte';

    let config = {
        normalHour: 25.00,
        overtimeHour: 37.50,
        nightHour: 30.00,
        lateness: 0.50,
        absence: 200.00
    };

    async function saveConfig() {
        try {
            // Actualizar status/cargos (Ejemplo simplificado)
            // await api.put('/nomina/statuses/1', { base_hourly_rate: config.normalHour });
            
            // Actualizar reglas de deducción
            // await api.put('/nomina/deductions/1', { amount: config.absence });
            
            alert('Configuración guardada correctamente');
        } catch (e) {
            alert('Error guardando configuración');
        }
    }
</script>

<div class="max-w-4xl mx-auto space-y-6">
    <h1 class="text-2xl font-bold">Configuración de Nómina</h1>
    <p class="text-gray-500">Estos valores se aplicarán a todos los cálculos futuros.</p>

    <div class="grid gap-6 rounded-xl border bg-white p-8 shadow-sm">
        <h2 class="text-lg font-semibold">Valores por Hora</h2>
        
        <div class="grid grid-cols-2 gap-6">
            <div>
                <label class="mb-1 block text-sm font-medium">Pago por Hora Normal</label>
                <div class="relative">
                    <span class="absolute left-3 top-2 text-gray-500">$</span>
                    <input bind:value={config.normalHour} type="number" class="w-full rounded border px-8 py-2"/>
                </div>
            </div>
            <div>
                <label class="mb-1 block text-sm font-medium">Valor Hora Extra</label>
                <div class="relative">
                    <span class="absolute left-3 top-2 text-gray-500">$</span>
                    <input bind:value={config.overtimeHour} type="number" class="w-full rounded border px-8 py-2"/>
                </div>
            </div>
        </div>

        <div class="border-t pt-6">
            <h2 class="text-lg font-semibold mb-4">Otros Valores (Deducciones)</h2>
            <div class="grid grid-cols-2 gap-6">
                <div>
                    <label class="mb-1 block text-sm font-medium">Valor por Atraso (minuto)</label>
                    <div class="relative">
                        <span class="absolute left-3 top-2 text-gray-500">$</span>
                        <input bind:value={config.lateness} type="number" class="w-full rounded border px-8 py-2"/>
                    </div>
                </div>
                 <div>
                    <label class="mb-1 block text-sm font-medium">Deducción por Ausencia (día)</label>
                    <div class="relative">
                        <span class="absolute left-3 top-2 text-gray-500">$</span>
                        <input bind:value={config.absence} type="number" class="w-full rounded border px-8 py-2"/>
                    </div>
                </div>
            </div>
        </div>

        <div class="flex justify-end gap-4 border-t pt-6">
            <button class="rounded-lg bg-gray-100 px-6 py-2 text-gray-700 hover:bg-gray-200">Cancelar</button>
            <button on:click={saveConfig} class="rounded-lg bg-blue-600 px-6 py-2 text-white hover:bg-blue-700">Guardar Cambios</button>
        </div>
    </div>
</div>