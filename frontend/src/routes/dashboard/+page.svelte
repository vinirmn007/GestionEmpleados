<script>
    import { onMount } from "svelte";
    import api from "$lib/utils/api";
    import {
        Users,
        UserCheck,
        UserX,
        Clock,
        Activity,
        ArrowRight,
    } from "lucide-svelte";

    let loading = true;
    let error = "";

    let totalEmployees = 0;
    let presentToday = 0;
    let absentToday = 0;
    let recentActivity = [];
    let departmentStats = [];

    async function loadDashboardData() {
        loading = true;
        try {
            const today = new Date().toISOString().split("T")[0];

            const usersRes = await api.get("/usuarios/all");
            const users = usersRes.data || [];
            totalEmployees = users.length;

            const deptCounts = {};
            users.forEach((u) => {
                const key = u.departamento || u.rol || "General";
                deptCounts[key] = (deptCounts[key] || 0) + 1;
            });

            departmentStats = Object.entries(deptCounts)
                .map(([name, count]) => ({
                    name,
                    count,
                    percent: (count / totalEmployees) * 100,
                }))
                .sort((a, b) => b.count - a.count);

            const attendanceRes = await api.get(
                `/attendance/reporte?target_date=${today}`,
            );
            const attendanceReport = attendanceRes.data || [];

            presentToday = attendanceReport.filter(
                (a) => a.estado === "Adentro",
            ).length;
            absentToday = attendanceReport.filter(
                (a) => a.estado === "Afuera",
            ).length;

            let allMarks = [];
            attendanceReport.forEach((u) => {
                if (u.marcas && u.marcas.length > 0) {
                    u.marcas.forEach((m) => {
                        allMarks.push({
                            user: u.nombre,
                            time: new Date(m),
                            type: "Marca",
                        });
                    });
                }
            });

            recentActivity = allMarks
                .sort((a, b) => b.time - a.time)
                .slice(0, 5)
                .map((m) => ({
                    ...m,
                    timeStr: m.time.toLocaleTimeString([], {
                        hour: "2-digit",
                        minute: "2-digit",
                    }),
                }));
        } catch (e) {
            console.error("Error loading dashboard", e);
            error = "No se pudieron cargar los datos del dashboard.";
        } finally {
            loading = false;
        }
    }

    onMount(() => {
        loadDashboardData();
    });
</script>

<div class="space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
        <div>
            <h1 class="text-2xl font-bold text-gray-800 dark:text-white">
                Dashboard General
            </h1>
            <p class="text-gray-500 dark:text-gray-400">
                Resumen de actividad y métricas clave.
            </p>
        </div>
        <div
            class="text-sm text-gray-500 dark:text-gray-400 bg-white dark:bg-gray-800 px-3 py-1 rounded-lg border border-gray-200 dark:border-gray-700"
        >
            {new Date().toLocaleDateString("es-ES", {
                weekday: "long",
                year: "numeric",
                month: "long",
                day: "numeric",
            })}
        </div>
    </div>

    {#if loading}
        <div class="flex h-64 items-center justify-center">
            <div
                class="h-8 w-8 animate-spin rounded-full border-4 border-blue-600 border-t-transparent"
            ></div>
        </div>
    {:else if error}
        <div
            class="rounded-xl bg-red-50 dark:bg-red-900/20 p-4 text-red-700 dark:text-red-400 border border-red-100 dark:border-red-800"
        >
            {error}
        </div>
    {:else}
        <!-- KPI Cards -->
        <div class="grid grid-cols-1 gap-6 md:grid-cols-3">
            <!-- Total Employees -->
            <div
                class="rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 p-6 shadow-sm"
            >
                <div class="flex items-center justify-between">
                    <div>
                        <p
                            class="text-sm font-medium text-gray-500 dark:text-gray-400"
                        >
                            Total Empleados
                        </p>
                        <p
                            class="text-3xl font-bold text-gray-900 dark:text-white mt-1"
                        >
                            {totalEmployees}
                        </p>
                    </div>
                    <div
                        class="rounded-full bg-blue-50 dark:bg-blue-900/30 p-3 text-blue-600 dark:text-blue-400"
                    >
                        <Users size={24} />
                    </div>
                </div>
                <div
                    class="mt-4 flex items-center text-sm text-green-600 dark:text-green-400"
                >
                    <Activity size={16} class="mr-1" />
                    <span class="font-medium">Activos</span>
                </div>
            </div>

            <!-- Present Today -->
            <div
                class="rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 p-6 shadow-sm"
            >
                <div class="flex items-center justify-between">
                    <div>
                        <p
                            class="text-sm font-medium text-gray-500 dark:text-gray-400"
                        >
                            Presentes Hoy
                        </p>
                        <p
                            class="text-3xl font-bold text-gray-900 dark:text-white mt-1"
                        >
                            {presentToday}
                        </p>
                    </div>
                    <div
                        class="rounded-full bg-green-50 dark:bg-green-900/30 p-3 text-green-600 dark:text-green-400"
                    >
                        <UserCheck size={24} />
                    </div>
                </div>
                <div
                    class="mt-4 w-full bg-gray-100 dark:bg-gray-700 rounded-full h-1.5"
                >
                    <div
                        class="bg-green-500 h-1.5 rounded-full"
                        style="width: {(presentToday / totalEmployees) * 100}%"
                    ></div>
                </div>
            </div>

            <!-- Absent/Late -->
            <div
                class="rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 p-6 shadow-sm"
            >
                <div class="flex items-center justify-between">
                    <div>
                        <p
                            class="text-sm font-medium text-gray-500 dark:text-gray-400"
                        >
                            Ausentes / Salida
                        </p>
                        <p
                            class="text-3xl font-bold text-gray-900 dark:text-white mt-1"
                        >
                            {absentToday}
                        </p>
                    </div>
                    <div
                        class="rounded-full bg-orange-50 dark:bg-orange-900/30 p-3 text-orange-600 dark:text-orange-400"
                    >
                        <UserX size={24} />
                    </div>
                </div>
                <div
                    class="mt-4 w-full bg-gray-100 dark:bg-gray-700 rounded-full h-1.5"
                >
                    <div
                        class="bg-orange-500 h-1.5 rounded-full"
                        style="width: {(absentToday / totalEmployees) * 100}%"
                    ></div>
                </div>
            </div>
        </div>

        <!-- Main Content Split -->
        <div class="grid grid-cols-1 gap-6 lg:grid-cols-3">
            <!-- Left Column: Activity & Charts -->
            <div class="lg:col-span-2 space-y-6">
                <!-- Recent Activity -->
                <div
                    class="rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 shadow-sm overflow-hidden"
                >
                    <div
                        class="border-b border-gray-100 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50 px-6 py-4 flex justify-between items-center"
                    >
                        <h3
                            class="font-semibold text-gray-800 dark:text-white flex items-center gap-2"
                        >
                            <Clock size={18} /> Actividad Reciente
                        </h3>
                        <a
                            href="/asistencia"
                            class="text-sm text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 font-medium flex items-center gap-1"
                        >
                            Ver todo <ArrowRight size={14} />
                        </a>
                    </div>
                    <div class="divide-y divide-gray-100 dark:divide-gray-700">
                        {#if recentActivity.length === 0}
                            <div
                                class="p-6 text-center text-gray-500 dark:text-gray-400"
                            >
                                No hay actividad registrada hoy.
                            </div>
                        {:else}
                            {#each recentActivity as activity}
                                <div
                                    class="flex items-center justify-between px-6 py-4 hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors"
                                >
                                    <div class="flex items-center gap-3">
                                        <div
                                            class="h-8 w-8 rounded-full bg-gray-200 dark:bg-gray-600 flex items-center justify-center text-xs font-bold text-gray-600 dark:text-gray-300"
                                        >
                                            {activity.user.charAt(0)}
                                        </div>
                                        <div>
                                            <p
                                                class="text-sm font-medium text-gray-900 dark:text-white"
                                            >
                                                {activity.user}
                                            </p>
                                            <p
                                                class="text-xs text-gray-500 dark:text-gray-400"
                                            >
                                                Marcación registrada
                                            </p>
                                        </div>
                                    </div>
                                    <span
                                        class="text-sm font-mono text-gray-600 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded"
                                    >
                                        {activity.timeStr}
                                    </span>
                                </div>
                            {/each}
                        {/if}
                    </div>
                </div>

                <!-- Department Distribution -->
                <div
                    class="rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 shadow-sm p-6"
                >
                    <h3
                        class="font-semibold text-gray-800 dark:text-white mb-6"
                    >
                        Distribución por Departamento/Rol
                    </h3>
                    <div class="space-y-4">
                        {#each departmentStats as dept}
                            <div>
                                <div class="flex justify-between text-sm mb-1">
                                    <span
                                        class="font-medium text-gray-700 dark:text-gray-300"
                                        >{dept.name}</span
                                    >
                                    <span
                                        class="text-gray-500 dark:text-gray-400"
                                        >{dept.count} empleados ({dept.percent.toFixed(
                                            0,
                                        )}%)</span
                                    >
                                </div>
                                <div
                                    class="w-full bg-gray-100 dark:bg-gray-700 rounded-full h-2.5"
                                >
                                    <div
                                        class="bg-indigo-600 h-2.5 rounded-full"
                                        style="width: {dept.percent}%"
                                    ></div>
                                </div>
                            </div>
                        {/each}
                    </div>
                </div>
            </div>

            <!-- Right Column: Quick Actions -->
            <div class="space-y-6">
                <div
                    class="rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 shadow-sm p-6"
                >
                    <h3
                        class="font-semibold text-gray-800 dark:text-white mb-4"
                    >
                        Accesos Directos
                    </h3>
                    <div class="grid grid-cols-1 gap-3">
                        <a
                            href="/empleados/nuevo"
                            class="flex items-center gap-3 p-3 rounded-lg border border-gray-200 dark:border-gray-600 hover:border-blue-300 dark:hover:border-blue-500 hover:bg-blue-50 dark:hover:bg-blue-900/20 transition-all group"
                        >
                            <div
                                class="p-2 bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 rounded-lg group-hover:bg-blue-200 dark:group-hover:bg-blue-900/50"
                            >
                                <Users size={18} />
                            </div>
                            <span
                                class="font-medium text-gray-700 dark:text-gray-300 group-hover:text-blue-800 dark:group-hover:text-blue-300"
                                >Nuevo Empleado</span
                            >
                        </a>
                        <a
                            href="/asistencia"
                            class="flex items-center gap-3 p-3 rounded-lg border border-gray-200 dark:border-gray-600 hover:border-green-300 dark:hover:border-green-500 hover:bg-green-50 dark:hover:bg-green-900/20 transition-all group"
                        >
                            <div
                                class="p-2 bg-green-100 dark:bg-green-900/30 text-green-600 dark:text-green-400 rounded-lg group-hover:bg-green-200 dark:group-hover:bg-green-900/50"
                            >
                                <Clock size={18} />
                            </div>
                            <span
                                class="font-medium text-gray-700 dark:text-gray-300 group-hover:text-green-800 dark:group-hover:text-green-300"
                                >Registrar Asistencia</span
                            >
                        </a>
                        <a
                            href="/nomina"
                            class="flex items-center gap-3 p-3 rounded-lg border border-gray-200 dark:border-gray-600 hover:border-purple-300 dark:hover:border-purple-500 hover:bg-purple-50 dark:hover:bg-purple-900/20 transition-all group"
                        >
                            <div
                                class="p-2 bg-purple-100 dark:bg-purple-900/30 text-purple-600 dark:text-purple-400 rounded-lg group-hover:bg-purple-200 dark:group-hover:bg-purple-900/50"
                            >
                                <Activity size={18} />
                            </div>
                            <span
                                class="font-medium text-gray-700 dark:text-gray-300 group-hover:text-purple-800 dark:group-hover:text-purple-300"
                                >Generar Nómina</span
                            >
                        </a>
                    </div>
                </div>

                <!-- System Status -->
                <div
                    class="rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 shadow-sm p-6"
                >
                    <h3
                        class="font-semibold text-gray-800 dark:text-white mb-4"
                    >
                        Estado del Sistema
                    </h3>
                    <div class="space-y-3">
                        <div class="flex items-center justify-between text-sm">
                            <span
                                class="flex items-center gap-2 text-gray-600 dark:text-gray-400"
                            >
                                <span class="h-2 w-2 rounded-full bg-green-500"
                                ></span> API Gateway
                            </span>
                            <span
                                class="text-green-600 dark:text-green-400 font-medium"
                                >Online</span
                            >
                        </div>
                        <div class="flex items-center justify-between text-sm">
                            <span
                                class="flex items-center gap-2 text-gray-600 dark:text-gray-400"
                            >
                                <span class="h-2 w-2 rounded-full bg-green-500"
                                ></span> Base de Datos
                            </span>
                            <span
                                class="text-green-600 dark:text-green-400 font-medium"
                                >Online</span
                            >
                        </div>
                        <div class="flex items-center justify-between text-sm">
                            <span
                                class="flex items-center gap-2 text-gray-600 dark:text-gray-400"
                            >
                                <span class="h-2 w-2 rounded-full bg-green-500"
                                ></span> Microservicios
                            </span>
                            <span
                                class="text-green-600 dark:text-green-400 font-medium"
                                >5/5 Activos</span
                            >
                        </div>
                    </div>
                </div>
            </div>
        </div>
    {/if}
</div>
