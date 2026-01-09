<script>
    import { Bell, Search } from 'lucide-svelte';
    
    // Recibimos el usuario como prop para mostrar su nombre/rol
    export let user = { role: 'Admin', email: 'usuario@empresa.com' };
</script>

<header class="flex h-16 items-center justify-between border-b border-gray-200 bg-white px-6 shadow-sm">
    
    <div class="hidden md:flex items-center rounded-lg bg-gray-50 px-3 py-2 w-96 border border-transparent focus-within:border-blue-300 focus-within:bg-white transition-all">
        <Search size={18} class="text-gray-400 mr-2" />
        <input 
            type="text" 
            placeholder="Buscar en el sistema..." 
            class="bg-transparent text-sm w-full outline-none text-gray-700 placeholder-gray-400"
        />
    </div>

    <div class="flex items-center gap-6">
        
        <button class="relative rounded-full p-2 text-gray-500 hover:bg-gray-100 transition-colors">
            <Bell size={20} />
            <span class="absolute right-2 top-2 h-2 w-2 rounded-full bg-red-500 border border-white"></span>
        </button>

        <div class="h-6 w-px bg-gray-200"></div>

        <div class="flex items-center gap-3">
            <div class="text-right hidden sm:block">
                <p class="text-sm font-semibold text-gray-800">Admin User</p>
                <p class="text-xs text-gray-500 capitalize">{user.role || 'Administrador'}</p>
            </div>
            
            <div class="h-10 w-10 overflow-hidden rounded-full border border-gray-200 bg-gray-100">
                <img 
                    src="https://ui-avatars.com/api/?name=Admin+User&background=0D8ABC&color=fff" 
                    alt="Avatar" 
                    class="h-full w-full object-cover"
                />
            </div>
        </div>
    </div>
</header>