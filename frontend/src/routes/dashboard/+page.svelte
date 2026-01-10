<script>
    import { onMount } from 'svelte';
    import api from '$lib/utils/api';
    import { Users, UserCheck, UserX, Clock, Activity, ArrowRight } from 'lucide-svelte';

    let loading = true;
    let error = '';

    // Data States
    let totalEmployees = 0;
    let presentToday = 0;
    let absentToday = 0;
    let recentActivity = [];
    let departmentStats = [];

    async function loadDashboardData() {
        loading = true;
        try {
            const today = new Date().toISOString().split('T')[0];

            // 1. Fetch Users (for Total count and Departments)
            // We fetch all to calculate stats locally since backend doesn't have specific stat endpoints yet
            const usersRes = await api.get('/usuarios/all');
            const users = usersRes.data || [];
            totalEmployees = users.length;

            // Calculate Department Distribution
            const deptCounts = {};
            users.forEach(u => {
                // Assuming 'rol' or a specific field maps to department/job. 
                // The user model has 'rol' (enum) and maybe 'cargo' (job_status_id).
                // Let's use 'rol' for now as a proxy if department isn't explicit, 
                // or check if there's a better field. 
                // Looking at previous files, 'departamento' was used in the mock data of empleados page.
                // Let's try to use 'departamento' if it exists, otherwise 'rol'.
                const key = u.departamento || u.rol || 'General';
                deptCounts[key] = (deptCounts[key] || 0) + 1;
            });

            departmentStats = Object.entries(deptCounts)
                .map(([name, count]) => ({ name, count, percent: (count / totalEmployees) * 100 }))
                .sort((a, b) => b.count - a.count);

            // 2. Fetch Attendance (for Present/Absent and Activity)
            // Note: /attendance/reporte returns a list of daily status
            const attendanceRes = await api.get(`/attendance/reporte?target_date=${today}`);
            const attendanceReport = attendanceRes.data || [];

            presentToday = attendanceReport.filter(a => a.estado === 'Adentro').length;
            absentToday = attendanceReport.filter(a => a.estado === 'Afuera').length;

            // For Recent Activity, we might need a different endpoint if 'reporte' only gives summary.
            // But 'reporte' returns { marcas: [...] }. We can extract the latest marks.
            // Alternatively, /attendance/history gives raw marks but requires user_id.
            // Let's construct "Recent Activity" from the report's latest marks for now.
            // We'll flatten all marks from all users today and sort them.
            let allMarks = [];
            attendanceReport.forEach(u => {
                if (u.marcas && u.marcas.length > 0) {
                    u.marcas.forEach(m => {
                        allMarks.push({
                            user: u.nombre,
                            time: new Date(m), // Assuming timestamp string
                            type: 'Marca' // We don't know in/out from just timestamp list easily without logic, but we can guess
                        });
                    });
                }
            });
            
            // Sort by time desc and take top 5
            recentActivity = allMarks
                .sort((a, b) => b.time - a.time)
                .slice(0, 5)
                .map(m => ({
                    ...m,
                    timeStr: m.time.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
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
            <h1 class="text-2xl font-bold text-gray-800">Dashboard General</h1>
            <p class="text-gray-500">Resumen de actividad y métricas clave.</p>
        </div>
        <div class="text-sm text-gray-500 bg-white px-3 py-1 rounded-lg border border-gray-200">
            {new Date().toLocaleDateString('es-ES', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}
        </div>
    </div>

    {#if loading}
        <div class="flex h-64 items-center justify-center">
            <div class="h-8 w-8 animate-spin rounded-full border-4 border-blue-600 border-t-transparent"></div>
        </div>
    {:else if error}
        <div class="rounded-xl bg-red-50 p-4 text-red-700 border border-red-100">
            {error}
        </div>
    {:else}
        <!-- KPI Cards -->
        <div class="grid grid-cols-1 gap-6 md:grid-cols-3">
            <!-- Total Employees -->
            <div class="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-sm font-medium text-gray-500">Total Empleados</p>
                        <p class="text-3xl font-bold text-gray-900 mt-1">{totalEmployees}</p>
                    </div>
                    <div class="rounded-full bg-blue-50 p-3 text-blue-600">
                        <Users size={24} />
                    </div>
                </div>
                <div class="mt-4 flex items-center text-sm text-green-600">
                    <Activity size={16} class="mr-1" />
                    <span class="font-medium">Activos</span>
                </div>
            </div>

            <!-- Present Today -->
            <div class="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-sm font-medium text-gray-500">Presentes Hoy</p>
                        <p class="text-3xl font-bold text-gray-900 mt-1">{presentToday}</p>
                    </div>
                    <div class="rounded-full bg-green-50 p-3 text-green-600">
                        <UserCheck size={24} />
                    </div>
                </div>
                <div class="mt-4 w-full bg-gray-100 rounded-full h-1.5">
                    <div class="bg-green-500 h-1.5 rounded-full" style="width: {(presentToday / totalEmployees) * 100}%"></div>
                </div>
            </div>

            <!-- Absent/Late -->
            <div class="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-sm font-medium text-gray-500">Ausentes / Salida</p>
                        <p class="text-3xl font-bold text-gray-900 mt-1">{absentToday}</p>
                    </div>
                    <div class="rounded-full bg-orange-50 p-3 text-orange-600">
                        <UserX size={24} />
                    </div>
                </div>
                <div class="mt-4 w-full bg-gray-100 rounded-full h-1.5">
                    <div class="bg-orange-500 h-1.5 rounded-full" style="width: {(absentToday / totalEmployees) * 100}%"></div>
                </div>
            </div>
        </div>

        <!-- Main Content Split -->
        <div class="grid grid-cols-1 gap-6 lg:grid-cols-3">
            
            <!-- Left Column: Activity & Charts -->
            <div class="lg:col-span-2 space-y-6">
                
                <!-- Recent Activity -->
                <div class="rounded-xl border border-gray-200 bg-white shadow-sm overflow-hidden">
                    <div class="border-b border-gray-100 bg-gray-50 px-6 py-4 flex justify-between items-center">
                        <h3 class="font-semibold text-gray-800 flex items-center gap-2">
                            <Clock size={18} /> Actividad Reciente
                        </h3>
                        <a href="/asistencia" class="text-sm text-blue-600 hover:text-blue-800 font-medium flex items-center gap-1">
                            Ver todo <ArrowRight size={14} />
                        </a>
                    </div>
                    <div class="divide-y divide-gray-100">
                        {#if recentActivity.length === 0}
                            <div class="p-6 text-center text-gray-500">No hay actividad registrada hoy.</div>
                        {:else}
                            {#each recentActivity as activity}
                                <div class="flex items-center justify-between px-6 py-4 hover:bg-gray-50 transition-colors">
                                    <div class="flex items-center gap-3">
                                        <div class="h-8 w-8 rounded-full bg-gray-200 flex items-center justify-center text-xs font-bold text-gray-600">
                                            {activity.user.charAt(0)}
                                        </div>
                                        <div>
                                            <p class="text-sm font-medium text-gray-900">{activity.user}</p>
                                            <p class="text-xs text-gray-500">Marcación registrada</p>
                                        </div>
                                    </div>
                                    <span class="text-sm font-mono text-gray-600 bg-gray-100 px-2 py-1 rounded">
                                        {activity.timeStr}
                                    </span>
                                </div>
                            {/each}
                        {/if}
                    </div>
                </div>

                <!-- Department Distribution -->
                <div class="rounded-xl border border-gray-200 bg-white shadow-sm p-6">
                    <h3 class="font-semibold text-gray-800 mb-6">Distribución por Departamento/Rol</h3>
                    <div class="space-y-4">
                        {#each departmentStats as dept}
                            <div>
                                <div class="flex justify-between text-sm mb-1">
                                    <span class="font-medium text-gray-700">{dept.name}</span>
                                    <span class="text-gray-500">{dept.count} empleados ({dept.percent.toFixed(0)}%)</span>
                                </div>
                                <div class="w-full bg-gray-100 rounded-full h-2.5">
                                    <div class="bg-indigo-600 h-2.5 rounded-full" style="width: {dept.percent}%"></div>
                                </div>
                            </div>
                        {/each}
                    </div>
                </div>

            </div>

            <!-- Right Column: Quick Actions -->
            <div class="space-y-6">
                <div class="rounded-xl border border-gray-200 bg-white shadow-sm p-6">
                    <h3 class="font-semibold text-gray-800 mb-4">Accesos Directos</h3>
                    <div class="grid grid-cols-1 gap-3">
                        <a href="/empleados/nuevo" class="flex items-center gap-3 p-3 rounded-lg border border-gray-200 hover:border-blue-300 hover:bg-blue-50 transition-all group">
                            <div class="p-2 bg-blue-100 text-blue-600 rounded-lg group-hover:bg-blue-200">
                                <Users size={18} />
                            </div>
                            <span class="font-medium text-gray-700 group-hover:text-blue-800">Nuevo Empleado</span>
                        </a>
                        <a href="/asistencia" class="flex items-center gap-3 p-3 rounded-lg border border-gray-200 hover:border-green-300 hover:bg-green-50 transition-all group">
                            <div class="p-2 bg-green-100 text-green-600 rounded-lg group-hover:bg-green-200">
                                <Clock size={18} />
                            </div>
                            <span class="font-medium text-gray-700 group-hover:text-green-800">Registrar Asistencia</span>
                        </a>
                        <a href="/nomina" class="flex items-center gap-3 p-3 rounded-lg border border-gray-200 hover:border-purple-300 hover:bg-purple-50 transition-all group">
                            <div class="p-2 bg-purple-100 text-purple-600 rounded-lg group-hover:bg-purple-200">
                                <Activity size={18} />
                            </div>
                            <span class="font-medium text-gray-700 group-hover:text-purple-800">Generar Nómina</span>
                        </a>
                    </div>
                </div>

                <!-- System Status (Mock) -->
                <div class="rounded-xl border border-gray-200 bg-white shadow-sm p-6">
                    <h3 class="font-semibold text-gray-800 mb-4">Estado del Sistema</h3>
                    <div class="space-y-3">
                        <div class="flex items-center justify-between text-sm">
                            <span class="flex items-center gap-2 text-gray-600">
                                <span class="h-2 w-2 rounded-full bg-green-500"></span> API Gateway
                            </span>
                            <span class="text-green-600 font-medium">Online</span>
                        </div>
                        <div class="flex items-center justify-between text-sm">
                            <span class="flex items-center gap-2 text-gray-600">
                                <span class="h-2 w-2 rounded-full bg-green-500"></span> Base de Datos
                            </span>
                            <span class="text-green-600 font-medium">Online</span>
                        </div>
                        <div class="flex items-center justify-between text-sm">
                            <span class="flex items-center gap-2 text-gray-600">
                                <span class="h-2 w-2 rounded-full bg-green-500"></span> Microservicios
                            </span>
                            <span class="text-green-600 font-medium">5/5 Activos</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    {/if}
</div>
