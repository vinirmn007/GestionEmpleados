<script>
    import { onMount, onDestroy } from "svelte";
    import api from "$lib/utils/api";
    import { Clock, LogIn, LogOut, CheckCircle2 } from "lucide-svelte";

    let time = new Date();
    let interval;
    let loading = false;
    let message = "";
    let error = "";
    let lastStatus = "Desconocido"; // Adentro / Afuera
    let todayMarks = 0;

    function updateTime() {
        time = new Date();
    }

    onMount(() => {
        interval = setInterval(updateTime, 1000);
        // Optional: Could fetch current status here if there was an endpoint for it
    });

    onDestroy(() => {
        clearInterval(interval);
    });

    async function registerMark() {
        loading = true;
        message = "";
        error = "";
        try {
            const response = await api.post("/attendance/mark", {});
            const data = response.data;

            lastStatus = data.current_status;
            todayMarks = data.todays_marks;
            message = `Marcación registrada exitosamente: ${time.toLocaleTimeString()}`;
        } catch (e) {
            console.error(e);
            error =
                "Error al registrar marcación: " +
                (e.response?.data?.detail || e.message);
        } finally {
            loading = false;
        }
    }
</script>

<div class="flex min-h-[80vh] flex-col items-center justify-center p-4">
    <div
        class="w-full max-w-md rounded-2xl bg-white p-8 shadow-xl dark:bg-gray-800 text-center border border-gray-100 dark:border-gray-700"
    >
        <div class="mb-6 flex justify-center text-blue-600 dark:text-blue-400">
            <Clock size={64} strokeWidth={1.5} />
        </div>

        <h1
            class="mb-2 text-4xl font-bold tracking-tight text-gray-900 dark:text-white"
        >
            {time.toLocaleTimeString()}
        </h1>
        <p class="mb-8 text-lg text-gray-500 dark:text-gray-400 capitalize">
            {time.toLocaleDateString(undefined, {
                weekday: "long",
                year: "numeric",
                month: "long",
                day: "numeric",
            })}
        </p>

        {#if message}
            <div
                class="mb-6 rounded-lg bg-green-50 p-4 text-green-700 dark:bg-green-900/30 dark:text-green-300 flex items-center justify-center gap-2 animate-pulse"
            >
                <CheckCircle2 size={20} />
                {message}
            </div>
        {/if}

        {#if error}
            <div
                class="mb-6 rounded-lg bg-red-50 p-4 text-red-700 dark:bg-red-900/30 dark:text-red-300"
            >
                {error}
            </div>
        {/if}

        <button
            on:click={registerMark}
            disabled={loading}
            class="group w-full relative flex items-center justify-center gap-3 overflow-hidden rounded-xl bg-blue-600 px-8 py-4 text-xl font-bold text-white transition-all hover:bg-blue-700 hover:scale-[1.02] active:scale-[0.98] disabled:opacity-70 disabled:cursor-not-allowed shadow-lg hover:shadow-blue-500/30"
        >
            {#if loading}
                <span class="animate-spin mr-2">⏳</span> Registrando...
            {:else}
                <LogIn size={24} />
                REGISTRAR ASISTENCIA
            {/if}

            <!-- Shine effect -->
            <div
                class="absolute inset-0 -translate-x-full group-hover:animate-[shimmer_1.5s_infinite] bg-gradient-to-r from-transparent via-white/20 to-transparent z-10"
            ></div>
        </button>

        {#if lastStatus !== "Desconocido"}
            <div
                class="mt-8 grid grid-cols-2 gap-4 border-t border-gray-100 pt-6 dark:border-gray-700"
            >
                <div class="text-center">
                    <p class="text-xs uppercase tracking-wider text-gray-400">
                        Estado Actual
                    </p>
                    <p
                        class="text-lg font-bold"
                        class:text-green-500={lastStatus === "Adentro"}
                        class:text-orange-500={lastStatus === "Afuera"}
                    >
                        {lastStatus}
                    </p>
                </div>
                <div class="text-center">
                    <p class="text-xs uppercase tracking-wider text-gray-400">
                        Marcaciones Hoy
                    </p>
                    <p class="text-lg font-bold text-gray-900 dark:text-white">
                        {todayMarks}
                    </p>
                </div>
            </div>
        {/if}
    </div>
</div>
