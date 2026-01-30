<script>
    import { onMount } from "svelte";
    import api from "$lib/utils/api";
    import {
        FileText,
        Calculator,
        Eye,
        Download,
        Search,
        Loader2,
        X,
        Save,
    } from "lucide-svelte";

    // Lista de empleados ACTIVOS
    let employees = [];
    let loading = true;
    let error = "";

    // Filtros
    let selectedMonth = new Date().getMonth() + 1;
    let selectedYear = new Date().getFullYear();

    // Modal de Detalle / Rol
    let showDetailModal = false;
    let selectedPayroll = null; // Datos completos del rol generado o calculado
    let isPreview = false; // True si es solo calculo, False si ya existe en BD
    let processing = false; // Calculando o generando PDF
    let activeCalculationId = null; // ID del empleado que se esta calculando

    // Datos auxiliares
    let months = [
        { val: 1, label: "Enero" },
        { val: 2, label: "Febrero" },
        { val: 3, label: "Marzo" },
        { val: 4, label: "Abril" },
        { val: 5, label: "Mayo" },
        { val: 6, label: "Junio" },
        { val: 7, label: "Julio" },
        { val: 8, label: "Agosto" },
        { val: 9, label: "Septiembre" },
        { val: 10, label: "Octubre" },
        { val: 11, label: "Noviembre" },
        { val: 12, label: "Diciembre" },
    ];

    async function loadData() {
        loading = true;
        try {
            // Cargar usuarios activos
            // La API de usuarios retorna todos, filtramos en front o back.
            // Usamos /usuarios/list (paginado) o /usuarios/all si existe.
            // Asumimos que queremos gestionar roles para todos.
            const response = await api.get("/usuarios/all"); // Asumimos que existe o usamos list con limit alto
            // Filtrar solo activos y con status
            employees = response.data.filter(
                (u) => u.activo && u.job_status_id,
            );

            // TODO: Consultar si ya tienen rol generado para el mes seleccionado?
            // Podríamos consultar el historial de nominas.
        } catch (e) {
            console.error(e);
            error = "Error al cargar empleados.";
        } finally {
            loading = false;
        }
    }

    async function calculatePayroll(user) {
        processing = true;
        activeCalculationId = user.id;
        try {
            // Llamamos a Reportes para PREVISUALIZAR (Calculo)
            // Endpoint: /reports/payroll-preview/{user_id}
            const response = await api.get(
                `/reports/payroll-preview/${user.id}`,
                {
                    params: {
                        start_date: `${selectedYear}-${String(selectedMonth).padStart(2, "0")}-01`,
                        end_date: `${selectedYear}-${String(selectedMonth).padStart(2, "0")}-30`, // Simplificado
                    },
                },
            );

            selectedPayroll = response.data;
            isPreview = true;
            showDetailModal = true;
        } catch (e) {
            console.error(e);
            alert(
                "Error al calcular rol: " +
                    (e.response?.data?.detail || e.message),
            );
        } finally {
            processing = false;
            activeCalculationId = null;
        }
    }

    function recalculateTotals() {
        if (!selectedPayroll) return;

        let totalRegular = 0;
        let totalOvertime = 0;

        selectedPayroll.details.forEach((day) => {
            const hours = parseFloat(day.hours_worked) || 0;
            if (hours > 8) {
                totalRegular += 8;
                totalOvertime += hours - 8;
            } else {
                totalRegular += hours;
            }
        });

        const rate = selectedPayroll.rate_per_hour || 0;
        const overtimeRate = selectedPayroll.overtime_rate || 0;
        const bonus = selectedPayroll.monthly_bonus || 0;

        const gross =
            totalRegular * rate + totalOvertime * overtimeRate + bonus;

        // Update local state
        selectedPayroll.total_regular_hours = totalRegular;
        selectedPayroll.total_overtime_hours = totalOvertime;
        selectedPayroll.estimated_gross_pay = parseFloat(gross.toFixed(2));
    }

    async function generateAndSave() {
        if (!selectedPayroll) return;
        processing = true;
        try {
            // Guardar en BD (Servicio Nomina)
            // POST /payrolls/generate
            const payload = {
                user_id: selectedPayroll.user_id,
                month: selectedMonth,
                year: selectedYear,
                override_data: {
                    estimated_gross_pay: selectedPayroll.estimated_gross_pay,
                    total_regular_hours: selectedPayroll.total_regular_hours,
                    total_overtime_hours: selectedPayroll.total_overtime_hours,
                    details: selectedPayroll.details, // Optional: if backend needs details to verify
                },
            };

            await api.post("/nomina/payrolls/generate", payload);
            alert("Rol de pago generado y guardado correctamente.");
            showDetailModal = false;
            // Recargar o marcar como generado
            loadData();
        } catch (e) {
            console.error(e);
            alert(
                "Error al guardar: " + (e.response?.data?.detail || e.message),
            );
        } finally {
            processing = false;
        }
    }

    async function downloadPDF() {
        if (!selectedPayroll) return;
        try {
            // POST /reports/pdf
            // Enviamos el objeto selectedPayroll completo
            const response = await api.post("/reports/pdf", selectedPayroll, {
                responseType: "blob",
            });

            // Crear link de descarga
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement("a");
            link.href = url;
            link.setAttribute(
                "download",
                `rol_${selectedPayroll.user_id}_${selectedMonth}_${selectedYear}.pdf`,
            );
            document.body.appendChild(link);
            link.click();
            link.remove();
        } catch (e) {
            console.error(e);
            alert("Error al descargar PDF");
        }
    }

    onMount(loadData);
</script>

<div
    class="mb-6 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4"
>
    <div>
        <h1 class="text-2xl font-bold text-gray-800 dark:text-white">
            Roles de Pago
        </h1>
        <p class="text-sm text-gray-500 dark:text-gray-400">
            Generación y consulta de roles mensuales.
        </p>
    </div>

    <div class="flex items-center gap-2">
        <select
            bind:value={selectedMonth}
            class="rounded-lg border border-gray-300 p-2 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
        >
            {#each months as m}
                <option value={m.val}>{m.label}</option>
            {/each}
        </select>
        <select
            bind:value={selectedYear}
            class="rounded-lg border border-gray-300 p-2 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
        >
            <option value={2024}>2024</option>
            <option value={2025}>2025</option>
            <option value={2026}>2026</option>
        </select>
        <button
            on:click={loadData}
            class="p-2 text-gray-600 hover:text-blue-600 dark:text-gray-300"
        >
            <Search size={20} />
        </button>
    </div>
</div>

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
                    <th class="px-6 py-3">Empleado</th>
                    <th class="px-6 py-3">Cédula</th>
                    <th class="px-6 py-3">Cargo</th>
                    <th class="px-6 py-3">Estado (Mes Actual)</th>
                    <th class="px-6 py-3 text-right">Acciones</th>
                </tr>
            </thead>
            <tbody>
                {#each employees as emp}
                    <tr
                        class="border-b bg-white hover:bg-gray-50 dark:border-gray-700 dark:bg-gray-800 dark:hover:bg-gray-700"
                    >
                        <td
                            class="px-6 py-4 font-medium text-gray-900 dark:text-white"
                            >{emp.nombre}</td
                        >
                        <td class="px-6 py-4">{emp.dni}</td>
                        <td class="px-6 py-4">Status #{emp.job_status_id}</td>
                        <td class="px-6 py-4">
                            <span
                                class="inline-flex items-center rounded-full bg-yellow-100 px-2.5 py-0.5 text-xs font-medium text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300"
                            >
                                Pendiente
                            </span>
                            <!-- TODO: Validar si ya existe generado -->
                        </td>
                        <td class="px-6 py-4 text-right">
                            <button
                                on:click={() => calculatePayroll(emp)}
                                disabled={processing}
                                class="inline-flex items-center gap-1 rounded-lg border border-blue-600 px-3 py-1.5 text-xs font-medium text-blue-600 hover:bg-blue-50 dark:border-blue-400 dark:text-blue-400 dark:hover:bg-blue-900/20 disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                                {#if activeCalculationId === emp.id}
                                    <Loader2 size={14} class="animate-spin" />
                                {:else}
                                    <Calculator size={14} />
                                {/if}
                                Calcular
                            </button>
                        </td>
                    </tr>
                {/each}
            </tbody>
        </table>
    </div>
{/if}

<!-- MODAL DE DETALLE -->
{#if showDetailModal && selectedPayroll}
    <div
        class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4"
    >
        <div
            class="w-full max-w-2xl rounded-xl bg-white p-6 shadow-xl dark:bg-gray-800 overflow-y-auto max-h-[90vh]"
        >
            <div class="mb-4 flex items-center justify-between">
                <h3 class="text-lg font-bold text-gray-900 dark:text-white">
                    Rol de Pago: {selectedPayroll.user_name}
                </h3>
                <button
                    on:click={() => (showDetailModal = false)}
                    class="text-gray-500 hover:text-gray-700"
                >
                    <X size={20} />
                </button>
            </div>

            <div class="grid grid-cols-1 gap-6 sm:grid-cols-2">
                <!-- Info Básica -->
                <div class="rounded-lg bg-gray-50 p-4 dark:bg-gray-700/50">
                    <h4
                        class="mb-2 font-semibold text-gray-900 dark:text-white"
                    >
                        Datos Empleado
                    </h4>
                    <p class="text-sm">
                        <strong>Cédula:</strong>
                        {selectedPayroll.dni}
                    </p>
                    <p class="text-sm">
                        <strong>Correo:</strong>
                        {selectedPayroll.email}
                    </p>
                    <p class="text-sm">
                        <strong>Cargo:</strong>
                        {selectedPayroll.job_status}
                    </p>
                    <p class="text-sm">
                        <strong>Cuenta:</strong>
                        {selectedPayroll.bank_account || "No registrada"}
                    </p>
                </div>

                <!-- Resumen Financiero -->
                <div class="rounded-lg bg-blue-50 p-4 dark:bg-blue-900/20">
                    <h4
                        class="mb-2 font-semibold text-blue-900 dark:text-blue-100"
                    >
                        Resumen Pago
                    </h4>
                    <div class="flex justify-between text-sm">
                        <span>Ingresos:</span>
                        <span class="font-medium text-green-600"
                            >${selectedPayroll.estimated_gross_pay}</span
                        >
                    </div>
                    <!-- Nota: Deducciones mostradas son un estimado o faltan calcular en el preview real -->
                    <div
                        class="mt-2 border-t border-blue-200 pt-2 flex justify-between text-base font-bold text-blue-800 dark:text-blue-200"
                    >
                        <span>A Recibir (Est.):</span>
                        <span
                            >${(
                                selectedPayroll.estimated_gross_pay * 0.9055
                            ).toFixed(2)}</span
                        >
                    </div>
                    <p class="text-xs text-blue-600 mt-1">
                        * Deducción IESS aprox 9.45%
                    </p>
                </div>
            </div>

            <!-- Detalle Diario -->
            <div class="mt-6">
                <h4 class="mb-2 font-semibold text-gray-900 dark:text-white">
                    Detalle de Asistencia
                </h4>
                <div
                    class="overflow-x-auto rounded-lg border border-gray-200 dark:border-gray-700"
                >
                    <table class="w-full text-left text-xs">
                        <thead class="bg-gray-100 dark:bg-gray-700">
                            <tr>
                                <th class="px-4 py-2">Fecha</th>
                                <th class="px-4 py-2">Estado</th>
                                <th class="px-4 py-2 text-right">Horas</th>
                            </tr>
                        </thead>
                        <tbody>
                            {#each selectedPayroll.details as day}
                                <tr
                                    class="border-t border-gray-100 dark:border-gray-700"
                                >
                                    <td class="px-4 py-2">{day.date}</td>
                                    <td class="px-4 py-2">{day.status}</td>
                                    <td class="px-4 py-2 text-right">
                                        <input
                                            type="number"
                                            step="0.1"
                                            min="0"
                                            bind:value={day.hours_worked}
                                            on:input={recalculateTotals}
                                            class="w-20 rounded border border-gray-300 p-1 text-right text-xs dark:bg-gray-700 dark:border-gray-600 dark:text-white"
                                        />
                                    </td>
                                </tr>
                            {/each}
                        </tbody>
                    </table>
                </div>
            </div>

            <div
                class="mt-6 flex justify-end gap-3 border-t border-gray-100 pt-4 dark:border-gray-700"
            >
                <button
                    type="button"
                    on:click={() => (showDetailModal = false)}
                    class="rounded-lg border border-gray-300 px-4 py-2 text-sm font-medium hover:bg-gray-50 dark:border-gray-600 dark:text-white dark:hover:bg-gray-700"
                >
                    Cerrar
                </button>

                <button
                    on:click={downloadPDF}
                    class="flex items-center gap-2 rounded-lg bg-gray-600 px-4 py-2 text-sm font-medium text-white hover:bg-gray-700"
                >
                    <Download size={16} /> PDF
                </button>

                {#if isPreview}
                    <button
                        on:click={generateAndSave}
                        disabled={processing}
                        class="flex items-center gap-2 rounded-lg bg-green-600 px-4 py-2 text-sm font-medium text-white hover:bg-green-700 disabled:opacity-75 disabled:cursor-not-allowed"
                    >
                        {#if processing && !activeCalculationId}
                            <Loader2 size={16} class="animate-spin" />
                        {:else}
                            <Save size={16} />
                        {/if}
                        Aprobar y Guardar
                    </button>
                {/if}
            </div>
        </div>
    </div>
{/if}
