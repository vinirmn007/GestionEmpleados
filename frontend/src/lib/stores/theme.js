import { writable } from 'svelte/store';
import { browser } from '$app/environment';

const storedTheme = browser ? localStorage.getItem('theme') : 'light';

export const theme = writable(storedTheme || 'light');

theme.subscribe((value) => {
    if (browser) {
        localStorage.setItem('theme', value);
        if (value === 'dark') {
            document.documentElement.classList.add('dark');
        } else {
            document.documentElement.classList.remove('dark');
        }
    }
});

export function toggleTheme() {
    theme.update((current) => (current === 'dark' ? 'light' : 'dark'));
}
