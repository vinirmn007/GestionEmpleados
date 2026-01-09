<script>
    import api from '$lib/utils/api';
    import { ArrowLeft, Save, Loader2 } from 'lucide-svelte';
    
    // Si estás usando SvelteKit:
    // import { goto } from '$app/navigation'; 
    // Si usas svelte-routing u otro router, ajusta la redirección al final.

    let loading = false;
    let error = '';
    let success = '';

    // Estado del formulario
    let formData = {
        nombre: '',
        dni: '',
        correo: '',
        celular: '',
        direccion: '',
        password: ''
    };

    async function handleSubmit() {
        loading = true;
        error = '';
        success = '';

        try {
            // Nota: Ajusta la URL '/usuarios' si tu backend espera '/empleados'
            // Enviamos el objeto tal cual, el backend pondrá rol="empleado" y hasheará el password
            const { data } = await api.post('/usuarios/create', formData); 
            
            success = `Empleado ${data.nombre} creado correctamente.`;
            
            // Limpiar formulario
            formData = {
                nombre: '', dni: '', correo: '', celular: '', direccion: '', password: ''
            };

            // Opcional: Redirigir después de 1.5 segundos
            setTimeout(() => {
                window.location.href = '/empleados'; // O usa goto('/empleados') si es SvelteKit
            }, 1500);

        } catch (e) {
            console.error(e);
            // Intentamos extraer el mensaje de error del backend (FastAPI suele devolver detail)
            if (e.response && e.response.data && e.response.data.detail) {
                error = e.response.data.detail;
            } else {
                error = "Error al conectar con el servidor. Intente nuevamente.";
            }
        } finally {
            loading = false;
        }
    }
</script>

<div class="mb-6 flex items-center justify-between">
    <div class="flex items-center gap-4">
        <a href="/empleados" class="rounded-lg p-2 text-gray-500 hover:bg-gray-100 hover:text-gray-700">
            <ArrowLeft size={24} />
        </a>
        <div>
            <h1 class="text-2xl font-bold text-gray-800">Nuevo Empleado</h1>
            <p class="text-sm text-gray-500">Complete la información para registrar un nuevo usuario.</p>
        </div>
    </div>
</div>

<div class="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
    
    {#if error}
        <div class="mb-6 rounded-lg bg-red-50 p-4 text-sm text-red-800 border border-red-200">
            <span class="font-bold">Error:</span> {error}
        </div>
    {/if}

    {#if success}
        <div class="mb-6 rounded-lg bg-green-50 p-4 text-sm text-green-800 border border-green-200">
            <span class="font-bold">¡Éxito!</span> {success} Redirigiendo...
        </div>
    {/if}

    <form on:submit|preventDefault={handleSubmit}>
        <div class="grid gap-6 mb-6 md:grid-cols-2">
            
            <div>
                <label for="nombre" class="mb-2 block text-sm font-medium text-gray-900">Nombre Completo</label>
                <input 
                    type="text" 
                    id="nombre" 
                    bind:value={formData.nombre} 
                    required
                    placeholder="Ej. Juan Pérez"
                    class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-gray-900 focus:border-blue-500 focus:ring-blue-500 focus:outline-none" 
                />
            </div>

            <div>
                <label for="dni" class="mb-2 block text-sm font-medium text-gray-900">DNI / Cédula</label>
                <input 
                    type="text" 
                    id="dni" 
                    bind:value={formData.dni} 
                    required
                    placeholder="Ej. 110451xxxx"
                    class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-gray-900 focus:border-blue-500 focus:ring-blue-500 focus:outline-none" 
                />
            </div>

            <div>
                <label for="correo" class="mb-2 block text-sm font-medium text-gray-900">Correo Electrónico</label>
                <input 
                    type="email" 
                    id="correo" 
                    bind:value={formData.correo} 
                    required
                    placeholder="nombre@empresa.com"
                    class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-gray-900 focus:border-blue-500 focus:ring-blue-500 focus:outline-none" 
                />
            </div>

            <div>
                <label for="celular" class="mb-2 block text-sm font-medium text-gray-900">Celular</label>
                <input 
                    type="tel" 
                    id="celular" 
                    bind:value={formData.celular} 
                    required
                    placeholder="09xxxxxxxx"
                    class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-gray-900 focus:border-blue-500 focus:ring-blue-500 focus:outline-none" 
                />
            </div>

            <div class="md:col-span-2">
                <label for="direccion" class="mb-2 block text-sm font-medium text-gray-900">Dirección Domiciliaria</label>
                <input 
                    type="text" 
                    id="direccion" 
                    bind:value={formData.direccion} 
                    required
                    placeholder="Calle Principal y Secundaria..."
                    class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-gray-900 focus:border-blue-500 focus:ring-blue-500 focus:outline-none" 
                />
            </div>

            <div class="md:col-span-2">
                <label for="password" class="mb-2 block text-sm font-medium text-gray-900">Contraseña Temporal</label>
                <input 
                    type="password" 
                    id="password" 
                    bind:value={formData.password} 
                    required
                    minlength="4"
                    placeholder="••••••••"
                    class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-gray-900 focus:border-blue-500 focus:ring-blue-500 focus:outline-none" 
                />
                <p class="mt-1 text-xs text-gray-500">El usuario podrá cambiar su contraseña al iniciar sesión por primera vez.</p>
            </div>
        </div>

        <div class="flex items-center justify-end gap-4 border-t border-gray-100 pt-6">
            <a 
                href="/empleados" 
                class="rounded-lg border border-gray-300 bg-white px-5 py-2.5 text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-4 focus:ring-gray-200"
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