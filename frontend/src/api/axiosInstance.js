import axios from 'axios';

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/',
});

// Interceptor de PETICIÓN: Inyectar el token
api.interceptors.request.use((config) => {
    let token = localStorage.getItem("access");

    if (token) {
        token = token.replace(/['"]+/g, '').trim();
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
}, (error) => {
    return Promise.reject(error);
});

// Interceptor de RESPUESTA: Manejar sesiones caducadas (401)
api.interceptors.response.use(
    (response) => response, // Si todo va bien, no hacemos nada
    (error) => {
        // Si el servidor responde 401 (Unauthorized)
        if (error.response && error.response.status === 401) {
            console.warn("Sesión caducada o token inválido. Redirigiendo al login...");
            
            // Limpiamos los datos de sesión
            localStorage.removeItem("access");
            localStorage.removeItem("refresh");

            // Redirigimos al usuario al login si no está ya allí
            if (!window.location.pathname.includes('/login')) {
                window.location.href = '/login';
            }
        }
        return Promise.reject(error);
    }
);

export default api;
