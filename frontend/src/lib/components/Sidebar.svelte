<script>
    import { page } from "$app/stores";
    import { auth } from "$lib/stores/auth";
    import { goto } from "$app/navigation";

    import {
        LayoutDashboard,
        Users,
        CalendarClock,
        ClipboardCheck,
        Banknote,
        BarChart3,
        Settings,
        LogOut,
        Briefcase,
        Menu,
        X,
        FileText,
        Fingerprint,
    } from "lucide-svelte";

    let isOpen = false;

    $: isActive = (path) => $page.url.pathname.startsWith(path);
    $: $page.url.pathname, (isOpen = false);

    function handleLogout() {
        auth.logout();
        goto("/login");
    }

    function toggleMenu() {
        isOpen = !isOpen;
    }
</script>

<button
    on:click={toggleMenu}
    class="fixed top-4 left-4 z-50 rounded-lg bg-white dark:bg-gray-800 p-2 text-gray-600 dark:text-gray-300 shadow-md md:hidden hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
    aria-label="Toggle Menu"
>
    {#if isOpen}
        <X size={24} />
    {:else}
        <Menu size={24} />
    {/if}
</button>

{#if isOpen}
    <div
        class="fixed inset-0 z-30 bg-black/50 backdrop-blur-sm transition-opacity md:hidden"
        on:click={() => (isOpen = false)}
    ></div>
{/if}

<aside
    class="
    fixed inset-y-0 left-0 z-40 flex h-screen w-64 flex-col border-r border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 transition-transform duration-300 ease-in-out
    md:static md:translate-x-0
    {isOpen ? 'translate-x-0' : '-translate-x-full'}
"
>
    <div
        class="flex h-16 items-center justify-between border-b border-gray-100 dark:border-gray-700 px-6"
    >
        <div class="flex items-center gap-3">
            <div
                class="flex h-8 w-8 items-center justify-center rounded bg-blue-600 text-white"
            >
                <Briefcase size={20} />
            </div>
            <span class="text-lg font-bold text-gray-800 dark:text-white"
                >HR System</span
            >
        </div>
        <button
            on:click={() => (isOpen = false)}
            class="text-gray-500 dark:text-gray-400 md:hidden"
        >
            <X size={20} />
        </button>
    </div>

    <nav class="flex-1 space-y-1 overflow-y-auto px-3 py-4">
        <a
            href="/dashboard"
            class="flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors
           {isActive('/dashboard')
                ? 'bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400'
                : 'text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 hover:text-gray-900 dark:hover:text-white'}"
        >
            <LayoutDashboard size={20} />
            <span>Dashboard</span>
        </a>

        <a
            href="/empleados"
            class="flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors
           {isActive('/empleados')
                ? 'bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400'
                : 'text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 hover:text-gray-900 dark:hover:text-white'}"
        >
            <Users size={20} />
            <span>Empleados</span>
        </a>

        <a
            href="/asistencia"
            class="flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors
           {isActive('/asistencia')
                ? 'bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400'
                : 'text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 hover:text-gray-900 dark:hover:text-white'}"
        >
            <ClipboardCheck size={20} />
            <span>Asistencia</span>
        </a>

        <a
            href="/marcar"
            class="flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors
           {isActive('/marcar')
                ? 'bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400'
                : 'text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 hover:text-gray-900 dark:hover:text-white'}"
        >
            <Fingerprint size={20} />
            <span>Marcar Asistencia</span>
        </a>

        <a
            href="/horarios"
            class="flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors
           {isActive('/horarios')
                ? 'bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400'
                : 'text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 hover:text-gray-900 dark:hover:text-white'}"
        >
            <CalendarClock size={20} />
            <span>Horarios</span>
        </a>

        <a
            href="/roles"
            class="flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors
           {isActive('/roles')
                ? 'bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400'
                : 'text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 hover:text-gray-900 dark:hover:text-white'}"
        >
            <FileText size={20} />
            <span>Roles de Pago</span>
        </a>

        <a
            href="/nomina"
            class="flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors
           {isActive('/nomina')
                ? 'bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400'
                : 'text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 hover:text-gray-900 dark:hover:text-white'}"
        >
            <Banknote size={20} />
            <span>Nómina</span>
        </a>

        <a
            href="/reportes"
            class="flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors
           {isActive('/reportes')
                ? 'bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400'
                : 'text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 hover:text-gray-900 dark:hover:text-white'}"
        >
            <BarChart3 size={20} />
            <span>Reportes</span>
        </a>

        <div class="my-2 border-t border-gray-100 dark:border-gray-700"></div>

        <a
            href="/nomina/configuracion"
            class="flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors
           {isActive('/nomina/configuracion')
                ? 'bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400'
                : 'text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 hover:text-gray-900 dark:hover:text-white'}"
        >
            <Settings size={20} />
            <span>Configuración</span>
        </a>

        <a
            href="/status"
            class="flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors
           {isActive('/status')
                ? 'bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400'
                : 'text-gray-600 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 hover:text-gray-900 dark:hover:text-white'}"
        >
            <Briefcase size={20} />
            <span>Gestión de Status</span>
        </a>
    </nav>

    <div class="border-t border-gray-200 dark:border-gray-700 p-4">
        <button
            on:click={handleLogout}
            class="flex w-full items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium text-red-600 dark:text-red-400 transition-colors hover:bg-red-50 dark:hover:bg-red-900/20"
        >
            <LogOut size={20} />
            <span>Cerrar Sesión</span>
        </button>
    </div>
</aside>
