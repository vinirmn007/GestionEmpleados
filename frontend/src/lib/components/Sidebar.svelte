<script>
    import { page } from '$app/stores';
    import { auth } from '$lib/stores/auth';
    import { goto } from '$app/navigation';
    
    // Iconos importados de lucide-svelte
    import { 
        LayoutDashboard, 
        Users, 
        CalendarClock, // Para Horarios
        ClipboardCheck, // Para Asistencia/Marcaciones
        Banknote,      // Para Nómina
        BarChart3,     // Para Reportes
        Settings, 
        LogOut,
        Briefcase
    } from 'lucide-svelte';

    // Función reactiva para saber si una ruta está activa
    $: isActive = (path) => $page.url.pathname.startsWith(path);

    function handleLogout() {
        auth.logout();
        goto('/login');
    }
</script>

<aside class="flex h-screen w-64 flex-col border-r border-gray-200 bg-white transition-all duration-300">
    <div class="flex h-16 items-center gap-3 border-b border-gray-100 px-6">
        <div class="flex h-8 w-8 items-center justify-center rounded bg-blue-600 text-white">
            <Briefcase size={20} />
        </div>
        <span class="text-lg font-bold text-gray-800">HR System</span>
    </div>

    <nav class="flex-1 space-y-1 overflow-y-auto px-3 py-4">
        
        <a href="/dashboard" 
           class="flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors 
           {isActive('/dashboard') ? 'bg-blue-50 text-blue-600' : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'}">
            <LayoutDashboard size={20} />
            <span>Dashboard</span>
        </a>

        <a href="/empleados" 
           class="flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors 
           {isActive('/empleados') ? 'bg-blue-50 text-blue-600' : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'}">
            <Users size={20} />
            <span>Empleados</span>
        </a>

        <a href="/asistencia" 
           class="flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors 
           {isActive('/asistencia') ? 'bg-blue-50 text-blue-600' : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'}">
            <ClipboardCheck size={20} />
            <span>Asistencia</span>
        </a>

        <a href="/horarios" 
           class="flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors 
           {isActive('/horarios') ? 'bg-blue-50 text-blue-600' : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'}">
            <CalendarClock size={20} />
            <span>Horarios</span>
        </a>

        <a href="/nomina" 
           class="flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors 
           {isActive('/nomina') ? 'bg-blue-50 text-blue-600' : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'}">
            <Banknote size={20} />
            <span>Nómina</span>
        </a>

        <a href="/reportes" 
           class="flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors 
           {isActive('/reportes') ? 'bg-blue-50 text-blue-600' : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'}">
            <BarChart3 size={20} />
            <span>Reportes</span>
        </a>

        <div class="my-2 border-t border-gray-100"></div>

        <a href="/nomina/configuracion" 
           class="flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors 
           {isActive('/nomina/configuracion') ? 'bg-blue-50 text-blue-600' : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'}">
            <Settings size={20} />
            <span>Configuración</span>
        </a>
    </nav>

    <div class="border-t border-gray-200 p-4">
        <button on:click={handleLogout} 
                class="flex w-full items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium text-red-600 transition-colors hover:bg-red-50">
            <LogOut size={20} />
            <span>Cerrar Sesión</span>
        </button>
    </div>
</aside>