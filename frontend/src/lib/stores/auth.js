import { writable } from 'svelte/store';
import { browser } from '$app/environment';

// Persistencia básica en localStorage
const storedToken = browser ? localStorage.getItem('token') : null;
const storedUser = browser ? JSON.parse(localStorage.getItem('user') || '{}') : {};

function createAuthStore() {
    const { subscribe, set, update } = writable({
        isAuthenticated: !!storedToken,
        token: storedToken,
        user: storedUser
    });

    return {
        subscribe,
        login: (token, userData) => {
            if (browser) {
                localStorage.setItem('token', token);
                localStorage.setItem('user', JSON.stringify(userData));
            }
            set({ isAuthenticated: true, token, user: userData });
        },
        logout: () => {
            if (browser) {
                localStorage.removeItem('token');
                localStorage.removeItem('user');
            }
            set({ isAuthenticated: false, token: null, user: {} });
        }
    };
}

export const auth = createAuthStore();