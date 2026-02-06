<script>
    import { Bell, Search, Sun, Moon, Accessibility } from "lucide-svelte";
    import { theme, toggleTheme } from "$lib/stores/theme";
    import { accessibility } from "$lib/stores/accessibility";
    import AccessibilityPanel from "./AccessibilityPanel.svelte";

    export let user = { role: "Admin", email: "usuario@empresa.com" };

    let showAccessibilityPanel = false;
</script>

<header
    class="flex h-16 items-center justify-between border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 px-6 shadow-sm"
>
    <div
        class="hidden md:flex items-center rounded-lg bg-gray-50 dark:bg-gray-700 px-3 py-2 w-96 border border-transparent focus-within:border-blue-300 dark:focus-within:border-blue-500 focus-within:bg-white dark:focus-within:bg-gray-600 transition-all"
    >
        <Search size={18} class="text-gray-400 dark:text-gray-300 mr-2" />
        <input
            type="text"
            placeholder="Buscar en el sistema..."
            class="bg-transparent text-sm w-full outline-none text-gray-700 dark:text-gray-200 placeholder-gray-400 dark:placeholder-gray-500"
        />
    </div>

    <div class="flex items-center gap-3">
        <!-- Accessibility Toggle -->
        <button
            on:click={() => (showAccessibilityPanel = !showAccessibilityPanel)}
            class="relative rounded-full p-2 text-gray-500 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
            title="Opciones de Accesibilidad"
            aria-label="Abrir panel de accesibilidad"
        >
            <Accessibility size={20} />
        </button>

        <!-- Theme Toggle -->
        <button
            on:click={toggleTheme}
            class="relative rounded-full p-2 text-gray-500 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
            title={$theme === "dark"
                ? "Cambiar a modo claro"
                : "Cambiar a modo oscuro"}
            aria-label={$theme === "dark"
                ? "Cambiar a modo claro"
                : "Cambiar a modo oscuro"}
        >
            {#if $theme === "dark"}
                <Sun size={20} />
            {:else}
                <Moon size={20} />
            {/if}
        </button>

        <button
            class="relative rounded-full p-2 text-gray-500 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
            aria-label="Notificaciones"
        >
            <Bell size={20} />
            <span
                class="absolute right-2 top-2 h-2 w-2 rounded-full bg-red-500 border border-white dark:border-gray-800"
            ></span>
        </button>

        <div class="h-6 w-px bg-gray-200 dark:bg-gray-600"></div>

        <div class="flex items-center gap-3">
            <div class="text-right hidden sm:block">
                <p
                    class="text-sm font-semibold text-gray-800 dark:text-gray-100"
                >
                    Admin User
                </p>
                <p class="text-xs text-gray-500 dark:text-gray-400 capitalize">
                    {user?.role || "Administrador"}
                </p>
            </div>

            <div
                class="h-10 w-10 overflow-hidden rounded-full border border-gray-200 dark:border-gray-600 bg-gray-100 dark:bg-gray-700"
            >
                <img
                    src="https://ui-avatars.com/api/?name=Admin+User&background=0D8ABC&color=fff"
                    alt="Avatar del usuario"
                    class="h-full w-full object-cover"
                />
            </div>
        </div>
    </div>
</header>

<AccessibilityPanel
    isOpen={showAccessibilityPanel}
    onClose={() => (showAccessibilityPanel = false)}
/>
