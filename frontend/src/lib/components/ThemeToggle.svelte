<script>
    import { onMount } from 'svelte';
    import { Moon, Sun } from 'lucide-svelte';

    let isDark = false;

    onMount(() => {
        // 1. Revisar preferencia guardada o preferencia del sistema
        const userPref = localStorage.getItem('theme');
        const systemPref = window.matchMedia('(prefers-color-scheme: dark)').matches;

        if (userPref === 'dark' || (!userPref && systemPref)) {
            isDark = true;
            document.documentElement.classList.add('dark');
        } else {
            isDark = false;
            document.documentElement.classList.remove('dark');
        }
    });

    function toggleTheme() {
        isDark = !isDark;
        if (isDark) {
            document.documentElement.classList.add('dark');
            localStorage.setItem('theme', 'dark');
        } else {
            document.documentElement.classList.remove('dark');
            localStorage.setItem('theme', 'light');
        }
    }
</script>

<button 
    on:click={toggleTheme}
    class="flex w-full items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors 
    text-gray-600 hover:bg-gray-50 hover:text-gray-900 
    dark:text-gray-300 dark:hover:bg-gray-800 dark:hover:text-white"
>
    {#if isDark}
        <Sun size={20} />
        <span>Modo Claro</span>
    {:else}
        <Moon size={20} />
        <span>Modo Oscuro</span>
    {/if}
</button>