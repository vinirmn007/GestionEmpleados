<script>
    import api from "$lib/utils/api";
    import { ArrowLeft, Save, Loader2 } from "lucide-svelte";

    let loading = false;
    let error = "";
    let success = "";

    let formData = {
        nombre: "",
        dni: "",
        correo: "",
        celular: "",
        direccion: "",
        password: "",
    };

    async function handleSubmit() {
        loading = true;
        error = "";
        success = "";

        try {
            const { data } = await api.post("/usuarios/create", formData);

            success = `Empleado ${data.nombre} creado correctamente.`;

            formData = {
                nombre: "",
                dni: "",
                correo: "",
                celular: "",
                direccion: "",
                password: "",
            };

            setTimeout(() => {
                window.location.href = "/empleados";
            }, 1500);
        } catch (e) {
            console.error(e);
            if (e.response && e.response.data && e.response.data.detail) {
                error = e.response.data.detail;
            } else {
                error =
                    "Error al conectar con el servidor. Intente nuevamente.";
            }
        } finally {
            loading = false;
        }
    }
</script>

<div class="mb-6 flex items-center justify-between">
    <div class="flex items-center gap-4">
        <a
            href="/empleados"
            class="rounded-lg p-2 text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 hover:text-gray-700 dark:hover:text-gray-200"
        >
            <ArrowLeft size={24} />
        </a>
        <div>
            <h1 class="text-2xl font-bold text-gray-800 dark:text-white">
                Nuevo Empleado
            </h1>
            <p class="text-sm text-gray-500 dark:text-gray-400">
                Complete la información para registrar un nuevo usuario.
            </p>
        </div>
    </div>
</div>

<div
    class="rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 p-6 shadow-sm"
>
    {#if error}
        <div
            class="mb-6 rounded-lg bg-red-50 dark:bg-red-900/20 p-4 text-sm text-red-800 dark:text-red-400 border border-red-200 dark:border-red-800"
        >
            <span class="font-bold">Error:</span>
            {error}
        </div>
    {/if}

    {#if success}
        <div
            class="mb-6 rounded-lg bg-green-50 dark:bg-green-900/20 p-4 text-sm text-green-800 dark:text-green-400 border border-green-200 dark:border-green-800"
        >
            <span class="font-bold">¡Éxito!</span>
            {success} Redirigiendo...
        </div>
    {/if}

    <form on:submit|preventDefault={handleSubmit}>
        <div class="grid gap-6 mb-6 md:grid-cols-2">
            <div>
                <label
                    for="nombre"
                    class="mb-2 block text-sm font-medium text-gray-900 dark:text-gray-200"
                    >Nombre Completo</label
                >
                <input
                    type="text"
                    id="nombre"
                    bind:value={formData.nombre}
                    required
                    placeholder="Ej. Juan Pérez"
                    class="block w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 p-2.5 text-gray-900 dark:text-white focus:border-blue-500 focus:ring-blue-500 focus:outline-none"
                />
            </div>

            <div>
                <label
                    for="dni"
                    class="mb-2 block text-sm font-medium text-gray-900 dark:text-gray-200"
                    >DNI / Cédula</label
                >
                <input
                    type="text"
                    id="dni"
                    bind:value={formData.dni}
                    required
                    placeholder="Ej. 110451xxxx"
                    class="block w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 p-2.5 text-gray-900 dark:text-white focus:border-blue-500 focus:ring-blue-500 focus:outline-none"
                />
            </div>

            <div>
                <label
                    for="correo"
                    class="mb-2 block text-sm font-medium text-gray-900 dark:text-gray-200"
                    >Correo Electrónico</label
                >
                <input
                    type="email"
                    id="correo"
                    bind:value={formData.correo}
                    required
                    placeholder="nombre@empresa.com"
                    class="block w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 p-2.5 text-gray-900 dark:text-white focus:border-blue-500 focus:ring-blue-500 focus:outline-none"
                />
            </div>

            <div>
                <label
                    for="celular"
                    class="mb-2 block text-sm font-medium text-gray-900 dark:text-gray-200"
                    >Celular</label
                >
                <input
                    type="tel"
                    id="celular"
                    bind:value={formData.celular}
                    required
                    placeholder="09xxxxxxxx"
                    class="block w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 p-2.5 text-gray-900 dark:text-white focus:border-blue-500 focus:ring-blue-500 focus:outline-none"
                />
            </div>

            <div class="md:col-span-2">
                <label
                    for="direccion"
                    class="mb-2 block text-sm font-medium text-gray-900 dark:text-gray-200"
                    >Dirección Domiciliaria</label
                >
                <input
                    type="text"
                    id="direccion"
                    bind:value={formData.direccion}
                    required
                    placeholder="Calle Principal y Secundaria..."
                    class="block w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 p-2.5 text-gray-900 dark:text-white focus:border-blue-500 focus:ring-blue-500 focus:outline-none"
                />
            </div>

            <div class="md:col-span-2">
                <label
                    for="password"
                    class="mb-2 block text-sm font-medium text-gray-900 dark:text-gray-200"
                    >Contraseña Temporal</label
                >
                <input
                    type="password"
                    id="password"
                    bind:value={formData.password}
                    required
                    minlength="4"
                    placeholder="••••••••"
                    class="block w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 p-2.5 text-gray-900 dark:text-white focus:border-blue-500 focus:ring-blue-500 focus:outline-none"
                />
                <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">
                    El usuario podrá cambiar su contraseña al iniciar sesión por
                    primera vez.
                </p>
            </div>
        </div>

        <div
            class="flex items-center justify-end gap-4 border-t border-gray-100 dark:border-gray-700 pt-6"
        >
            <a
                href="/empleados"
                class="rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 px-5 py-2.5 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-600 focus:outline-none focus:ring-4 focus:ring-gray-200 dark:focus:ring-gray-700"
            >
                Cancelar
            </a>

            <button
                type="submit"
                disabled={loading}
                class="flex items-center gap-2 rounded-lg bg-blue-600 px-5 py-2.5 text-sm font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-4 focus:ring-blue-300 disabled:opacity-50 disabled:cursor-not-allowed"
            >
                {#if loading}
                    <Loader2 class="animate-spin" size={18} />
                    Guardando...
                {:else}
                    <Save size={18} />
                    Guardar Empleado
                {/if}
            </button>
        </div>
    </form>
</div>
