import axios from 'axios';
import { goto } from '$app/navigation';
import { auth } from '$lib/stores/auth';
import { get } from 'svelte/store';

// URL del Kong Gateway
const API_URL = 'http://localhost:8000'; 

const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json'
    }
});

// Interceptor para inyectar token
api.interceptors.request.use((config) => {
    const token = get(auth).token;
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

// Interceptor para manejar errores (401 Expired)
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response && error.response.status === 401) {
            auth.logout(); // Limpiar store
            goto('/login');
        }
        return Promise.reject(error);
    }
);

export default api;