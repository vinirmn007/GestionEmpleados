<script>
    import {
        accessibility,
        setFontSize,
        toggleHighContrast,
        toggleReducedMotion,
        toggleUnderlineLinks,
        resetAccessibility,
    } from "$lib/stores/accessibility";
    import { Eye, Type, Zap, Link2, RotateCcw, X } from "lucide-svelte";

    export let isOpen = false;
    export let onClose = () => {};
</script>

{#if isOpen}
    <!-- Backdrop -->
    <div class="fixed inset-0 bg-black/50 z-50" on:click={onClose}></div>

    <!-- Panel -->
    <div
        class="fixed right-4 top-20 w-80 bg-white dark:bg-gray-800 rounded-xl shadow-2xl border border-gray-200 dark:border-gray-700 z-50 overflow-hidden"
    >
        <div
            class="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50"
        >
            <h2
                class="text-lg font-bold text-gray-800 dark:text-white flex items-center gap-2"
            >
                <Eye size={20} /> Accesibilidad
            </h2>
            <button
                on:click={onClose}
                class="p-1 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-700 text-gray-500 dark:text-gray-400"
            >
                <X size={20} />
            </button>
        </div>

        <div class="p-4 space-y-5">
            <!-- Font Size -->
            <div>
                <label
                    class="flex items-center gap-2 text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
                >
                    <Type size={16} /> Tamaño de Texto
                </label>
                <div class="flex gap-2">
                    <button
                        on:click={() => setFontSize("normal")}
                        class="flex-1 px-3 py-2 rounded-lg text-sm font-medium transition-colors
                        {$accessibility.fontSize === 'normal'
                            ? 'bg-blue-600 text-white'
                            : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'}"
                    >
                        Normal
                    </button>
                    <button
                        on:click={() => setFontSize("large")}
                        class="flex-1 px-3 py-2 rounded-lg text-sm font-medium transition-colors
                        {$accessibility.fontSize === 'large'
                            ? 'bg-blue-600 text-white'
                            : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'}"
                    >
                        Grande
                    </button>
                    <button
                        on:click={() => setFontSize("xlarge")}
                        class="flex-1 px-3 py-2 rounded-lg text-sm font-medium transition-colors
                        {$accessibility.fontSize === 'xlarge'
                            ? 'bg-blue-600 text-white'
                            : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'}"
                    >
                        Muy Grande
                    </button>
                </div>
            </div>

            <!-- High Contrast -->
            <div class="flex items-center justify-between">
                <label
                    class="flex items-center gap-2 text-sm font-medium text-gray-700 dark:text-gray-300"
                >
                    <Eye size={16} /> Alto Contraste
                </label>
                <button
                    on:click={toggleHighContrast}
                    class="relative w-12 h-6 rounded-full transition-colors {$accessibility.highContrast
                        ? 'bg-blue-600'
                        : 'bg-gray-300 dark:bg-gray-600'}"
                >
                    <span
                        class="absolute top-1 left-1 w-4 h-4 bg-white rounded-full shadow transition-transform {$accessibility.highContrast
                            ? 'translate-x-6'
                            : ''}"
                    ></span>
                </button>
            </div>

            <!-- Reduced Motion -->
            <div class="flex items-center justify-between">
                <label
                    class="flex items-center gap-2 text-sm font-medium text-gray-700 dark:text-gray-300"
                >
                    <Zap size={16} /> Reducir Animaciones
                </label>
                <button
                    on:click={toggleReducedMotion}
                    class="relative w-12 h-6 rounded-full transition-colors {$accessibility.reducedMotion
                        ? 'bg-blue-600'
                        : 'bg-gray-300 dark:bg-gray-600'}"
                >
                    <span
                        class="absolute top-1 left-1 w-4 h-4 bg-white rounded-full shadow transition-transform {$accessibility.reducedMotion
                            ? 'translate-x-6'
                            : ''}"
                    ></span>
                </button>
            </div>

            <!-- Underline Links -->
            <div class="flex items-center justify-between">
                <label
                    class="flex items-center gap-2 text-sm font-medium text-gray-700 dark:text-gray-300"
                >
                    <Link2 size={16} /> Subrayar Enlaces
                </label>
                <button
                    on:click={toggleUnderlineLinks}
                    class="relative w-12 h-6 rounded-full transition-colors {$accessibility.underlineLinks
                        ? 'bg-blue-600'
                        : 'bg-gray-300 dark:bg-gray-600'}"
                >
                    <span
                        class="absolute top-1 left-1 w-4 h-4 bg-white rounded-full shadow transition-transform {$accessibility.underlineLinks
                            ? 'translate-x-6'
                            : ''}"
                    ></span>
                </button>
            </div>

            <!-- Reset Button -->
            <button
                on:click={resetAccessibility}
                class="w-full flex items-center justify-center gap-2 px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors text-sm font-medium"
            >
                <RotateCcw size={16} /> Restablecer Valores
            </button>
        </div>
    </div>
{/if}
