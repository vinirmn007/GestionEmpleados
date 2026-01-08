<script>
    import api from '$lib/utils/api';
    import { auth } from '$lib/stores/auth';
    import { goto } from '$app/navigation';
    import { jwtDecode } from "jwt-decode";

    let email = '';
    let password = '';
    let error = '';
    let loading = false;

    async function handleLogin() {
        loading = true;
        error = '';
        try {
            // Llama a: Kong -> Auth Service -> /auth/login
            const { data } = await api.post('/auth/auth/login', { email, password });
            
            // Decodificar token para obtener info del usuario si es necesario
            const decoded = jwtDecode(data.access_token);
            
            auth.login(data.access_token, { 
                id: decoded.sub, 
                role: decoded.roles 
            });
            
            goto('/dashboard');
        } catch (e) {
            error = 'Credenciales incorrectas o error en el servidor';
        } finally {
            loading = false;
        }
    }
</script>

<div class="flex h-screen w-full">
    <div class="hidden w-1/2 bg-gray-900 lg:block relative overflow-hidden">
        <img src="/path-to-plant-image.jpg" alt="Office" class="absolute inset-0 h-full w-full object-cover opacity-80"/>
        <div class="absolute bottom-20 left-10 text-white p-8">
            <h1 class="text-4xl font-bold mb-4">Impulsando el futuro del trabajo, juntos.</h1>
            <p class="text-lg text-gray-200">Nuestra plataforma centraliza la gestión.</p>
        </div>
    </div>

    <div class="flex w-full flex-col justify-center px-8 lg:w-1/2 lg:px-24 bg-white">
        <div class="mb-8">
            <h2 class="text-3xl font-bold text-gray-900">Bienvenido de nuevo</h2>
            <p class="text-gray-500 mt-2">Inicia sesión en tu cuenta para continuar.</p>
        </div>

        <form on:submit|preventDefault={handleLogin} class="space-y-6">
            <div>
                <label class="block text-sm font-medium text-gray-700">Usuario / Email</label>
                <input bind:value={email} type="email" required class="mt-1 w-full rounded-md border border-gray-300 px-4 py-3 focus:border-blue-500 focus:ring-blue-500"/>
            </div>

            <div>
                <label class="block text-sm font-medium text-gray-700">Contraseña</label>
                <input bind:value={password} type="password" required class="mt-1 w-full rounded-md border border-gray-300 px-4 py-3 focus:border-blue-500 focus:ring-blue-500"/>
            </div>

            {#if error}
                <p class="text-red-500 text-sm">{error}</p>
            {/if}

            <button type="submit" disabled={loading} class="w-full rounded-md bg-blue-700 py-3 text-white font-semibold hover:bg-blue-800 transition disabled:opacity-50">
                {loading ? 'Cargando...' : 'Acceder'}
            </button>
        </form>
    </div>
</div>