<!-- 
<script>
	import './layout.css';
	import favicon from '$lib/assets/favicon.svg';

	let { children } = $props();
</script>

<svelte:head><link rel="icon" href={favicon} /></svelte:head>
{@render children()}
-->

<script>
    import "./layout.css";
    import favicon from "$lib/assets/favicon.svg";

    import { page } from "$app/stores";
    import { auth } from "$lib/stores/auth";
    import { theme } from "$lib/stores/theme";
    import { accessibility } from "$lib/stores/accessibility";
    import { goto } from "$app/navigation";
    import { onMount } from "svelte";
    import Sidebar from "$lib/components/Sidebar.svelte";
    import Navbar from "$lib/components/Navbar.svelte";

    $: isLoginPage = $page.url.pathname === "/login";

    onMount(() => {
        // Initialize theme on mount
        if ($theme === "dark") {
            document.documentElement.classList.add("dark");
        }

        // Initialize accessibility settings
        document.documentElement.classList.add(
            `text-${$accessibility.fontSize}`,
        );
        if ($accessibility.highContrast)
            document.documentElement.classList.add("high-contrast");
        if ($accessibility.reducedMotion)
            document.documentElement.classList.add("reduce-motion");
        if ($accessibility.underlineLinks)
            document.documentElement.classList.add("underline-links");

        if (!$auth.isAuthenticated && !isLoginPage) {
            goto("/login");
        }
    });
</script>

{#if isLoginPage}
    <slot />
{:else}
    <div class="flex h-screen bg-gray-50 dark:bg-gray-900">
        <Sidebar />
        <div class="flex-1 flex flex-col overflow-hidden">
            <Navbar user={$auth.user} />
            <main
                class="flex-1 overflow-x-hidden overflow-y-auto bg-gray-50 dark:bg-gray-900 p-6"
            >
                <slot />
            </main>
        </div>
    </div>
{/if}
